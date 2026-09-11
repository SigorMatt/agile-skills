---
status: recorded
---

# Refinement Q&A — WI-0005

`status: recorded`, after three rounds. Round 1's five questions came back answered on 2026-09-11
and `## Answers — round 1` carries them verbatim. Round 2 rewrote the criteria against them,
decided what its own licences reached, and filed three things it could not settle without the
stakeholder — `Q-006`, `Q-007` and `Q-008`. Those three came back on the same day and
`## Answers — round 2` carries them verbatim; `answer-questions` propagated them into `item.md`
(AC1, AC16, AC17, AC18) and into `docs/product/vision.md` v6. **Round 3 asked nothing further**,
walked the Definition of Ready against the eighteen criteria those answers produced, appended two
criteria for what they left unconstrained, and reached Ready. The field moved from `agenda` to
`recorded` in that round, which is what R8 reads: the exchange below is a finished conversation
rather than a plan for one.

Every question this item ever put to the stakeholder is `status: answered`. Nothing is
`[unresolved]`.

## What the Definition of Ready says is missing

Read criterion by criterion against `spec/dor-dod.md` §1, before the questions were written.

| # | Verdict | Why |
|---|---------|-----|
| R1 | pass | `item.md` frontmatter is complete; `type`, `epic` and `priority` are set. `validate-workspace` agrees. |
| R2 | pass | `## Story` names the role (a person budgeting their own money at a terminal), the capability (correct a spend already recorded) and the outcome (*"so that a mistyped amount does not stay in my figures"*). |
| R3 | pass | Five criteria, labelled `AC1`–`AC5`, each a checkbox. |
| R4 | **fail** | AC1 says *"There is an `envel` command that changes a spend that was already recorded"* and names no command, no arguments and no way of saying **which** spend. AC2 and AC3 inherit that gap: neither can be observed until there is a line to type. AC4's *"a spend that does not exist"* is undecidable for the same reason — nothing defines what naming a spend even looks like. This is Q-001. |
| R5 | pass | Three exclusions, and the first (correcting a move) is one a reader would reasonably assume was included. |
| R6 | **fail by construction** | Five blocking questions are now open on this item. This is the criterion that is failing *because* refinement is in progress, and it clears when they are answered. |
| R7 | pass | `depends-on` is empty. `WI-0002`, which this item needs for there to be a spend to correct, is `done`, so the dependency is satisfied whether or not it is written into the frontmatter. Recording it belongs with the criteria rewrite in round 2. |
| R8 | **fail** | This file declares `status: agenda`. That is the honest state and R8 reads the field precisely so that an agenda cannot pass an item to `ready` by existing. |
| R9 | **unresolved** | Whether this is one coherent change depends on Q-002, Q-003 and Q-005. Amount-only corrections on spends is one small change; correcting four fields, removing spends, and correcting income as well is plausibly two or three. The split, if there is one, is decided in round 2 from the answers — not guessed at now. |
| R10 | **fail** | The behaviours this item introduces have no stated combinations, because the behaviours themselves are not yet chosen. Q-001 through Q-005 are precisely the axes: how a spend is named, which fields move, whether removal exists, what happens below zero, and whether income is included. |
| R11 | pass | No criterion on this item counts anything. Nothing to measure. |
| R12 | pass, vacuously | No `[assumed]` answer has been recorded on this item yet, so no delegation has been spent. One is anticipated and named below, so that when it is spent it is not spent silently. |

## Questions put to the stakeholder — round 1

Filed as `questions/Q-001.md` through `questions/Q-005.md`, all `addressed-to: human`,
all `blocking: true`, all `status: open`. They are five artifacts and one conversation: each
`## Context` opens with the same frame — *"`WI-0005`, round 1, question N of 5"* — and Q-005
says that is all of them for now (`spec/question.md` §2).

1. **Q-001 — how do you point at the spend you want to correct?** The item's own `## Notes` call
   this *"the open point that matters most"*, and they are right: nothing in this tool can show
   an individual spend, because `EP-001/Q-003` ruled them out of the only report there is. Four
   options, from a printed reference that needs `WI-0006` built, down to always correcting the
   most recent spend.
2. **Q-002 — which of a spend's four parts can be corrected?** Amount only; amount, date and
   description; or all four including the envelope. The date is the one that decides which
   monthly summary a spend lands in, so it carries more weight than the amount they used as
   their example.
3. **Q-003 — can a spend be removed altogether?** A duplicate is the one mistake correcting
   cannot repair. Their `WI-0001/Q-001` answer (*"nothing should ever be able to wipe money out
   of an envelope by accident"*) and their `EP-001/Q-005` answer pull opposite ways, so it is
   theirs to settle.
4. **Q-004 — may a correction take an envelope below zero?** `EP-001/Q-002` refuses an overspend
   at the moment of recording and is silent about the moment of correcting, and the two moments
   differ in a way that matters: the money in a correction has already left the house.
5. **Q-005 — can income be corrected too?** This is the cross-answer one. At `WI-0001/Q-003`
   they refused a negative income *on the grounds that* corrections were coming; if corrections
   reach only spends, a mistyped income has no route back and that reasoning is left without the
   thing it traded for.

## Why these five went to the stakeholder and nothing else did

`refine` step 3, applied question by question. Each of the five changes what the software
promises or what they would notice, and none of them has an answer that would be the same
whoever the stakeholder was:

- Q-001 changes what they type every time they fix a typo, and it decides whether `WI-0006` is
  work this epic needs or work nobody asked for.
- Q-002, Q-003 and Q-005 are scope: what can be put right and what is permanent.
- Q-004 is a promise about their data — the *"I don't want to see a negative envelope"* rule, at
  a moment their own answer did not reach.

One decision that is **not** going to them, recorded here so that the licence is visible when it
is spent rather than after:

- **The spelling of the correction command** — the subcommand's name, whether the reference is a
  plain word or a named option, the exact wording of a refusal. That is settled by their answer
  at `WI-0003/Q-004`: *"I'd rather everything in this tool be typed the same way than have one
  command that's special."* It cannot be decided until Q-001 says what the command takes, so it
  is round 2's, and when it is taken it will be recorded as an `[assumed]` answer carrying
  `**Under delegation:** WI-0003/Q-004 — argument style: a plain word for the argument a command
  normally takes, a named option for the one it rarely does` (R12).

Nothing on this item was routed to `plan` as an implementation-only question. The reason is
worth writing down: the hard part of this item — how one recorded spend is referred to — looks
like a design question and is not one. Every mechanism for it is visible on the command line, so
`plan` choosing it would be `plan` choosing what the stakeholder types.

## What happens next

The item moved to `awaiting-answer` with `resume-to: draft`. All five replies have now arrived and
`answer-questions` has propagated them; the item returns to `draft`. `refine` then runs a second
round, rewrites `AC1`–`AC10` against the answers, decides whether R9 requires a split, puts the
two things round 1's answers left open to the stakeholder (below), records the delegation named
above, and sets this file to `status: recorded` with the exchange verbatim.

## Answers — round 1

Received 2026-09-11, all five, verbatim. Consumed by `answer-questions`
(`questions/Q-001.md` … `Q-005.md`, each `status: answered`, `answered-by: human`).

**Q-001 — how do you point at the spend you want to fix?** → **A**, a short reference number.

> [human] A. I find these mistakes a couple of days after the month has ended with the statement in
> front of me, so an option that only reaches the last spend, or a number that scrolled off the
> screen a week ago, is no use to me. Give each spend a short number I can read off and type back.
> That does mean the listing command has to exist, and I am saying yes to that separately.

**Q-002 — which of a spend's four parts can be corrected?** → **C**, all four.

> [human] C — all four. If I typed the line wrong I want to fix the line, and with ten envelopes,
> putting the Saturday shop against "eating out" instead of "groceries" is a mistake I will
> certainly make. That is still fixing a spend, not fixing a move: a move stays unfixable, exactly
> as I decided before.

**Q-003 — can a spend be removed altogether?** → **B**, yes, its own command, saying what it took.

> [human] B — yes, and have it tell me what it took out. Recording the same shop twice is the one
> mistake I cannot correct my way out of, and I don't want a zero sitting in there pretending to be
> a spend. Don't make it stop and ask me to confirm; just say plainly what went and what the
> envelope holds now.

**Q-004 — may a correction take an envelope below zero?** → **C**, refused, and told how short.

> [human] C. No negative envelopes anywhere in this tool, and that includes here — refuse it and
> tell me how much short I am, so I can move the money across and type the correction again. Doing
> it in two steps is fine; seeing a minus number is not.

**Q-005 — can income be corrected too?** → **B**, spends and income; not moves.

> [human] B — spends and income. I turned down the negative income on the understanding that proper
> corrections were coming, so corrections had better reach an income; a payslip typed with the
> wrong number of noughts is worse than a mistyped shop. Not moves — that stays as I decided it.

## Cross-answer check — round 1, on the replies

Written on each question file as it was consumed; collected here so a reader of this item's
refinement story passes through it. The full per-ID verdicts are in the `## Cross-answer check`
section of each question.

- **No conflict was found**, on any of the five. The pair round 1 filed the question *for* —
  `WI-0001/Q-003`, the negative income refused *because* corrections were coming, against
  `EP-001/Q-005`, which named a spend — was resolved **by the stakeholder** at `Q-005` rather than
  by us: they chose B and gave that same reasoning back as the reason. That is ADR-0008 §3's
  intended outcome, and it is why round 1 filed the question instead of reconciling the two
  sentences here.
- The answer to `Q-002` and the answer to `Q-005` each restate `WI-0004/Q-001` — *"I can fix a
  spend afterwards and I can't fix a move"* — unprompted and in their own words. `WI-0004` is
  built and closed on that sentence and nothing here disturbs it.
- The answer to `Q-004` applies `EP-001/Q-002`'s no-negative-envelope rule to a moment that answer
  did not reach, and the stakeholder says so explicitly. Recording a fresh spend is untouched.
- The answer to `Q-001` leaves `EP-001/Q-003` — *"I definitely don't want every individual spend
  listed"* — intact: the reference is read off a command asked for by name, and the monthly
  summary keeps its four figures per envelope. The stakeholder made the same distinction again in
  `WI-0006/Q-001`'s reply.

## What round 1's answers left for round 2

Two things, both recorded in `item.md`'s `## Notes` and neither of them filed as a question by
`answer-questions`, because this item returns to `draft` and `refine` is the skill that asks:

1. **Whether an income can be removed as well as corrected.** `Q-003` asked about removing a
   *spend* and the reply names a spend; `Q-005` extends *correcting* to income and is silent about
   removing one. A duplicated payslip is the same mistake as a duplicated shop, so the gap is real.
   AC8 is deliberately written about a spend until the stakeholder settles it.
2. **Whether the reference of `Q-001` is per-envelope or global across the store.** `Q-001`'s
   example shows `envel spends groceries` printing `7`, which reads as per-envelope; the
   stakeholder's reply to `WI-0006/Q-003` asks for a listing with no envelope named, where a
   per-envelope number would be ambiguous. This is a question about what they type, not an
   implementation detail, which is why it is not `plan`'s.

And two that are round 2's own work rather than the stakeholder's:

3. **Whether R9 requires a split.** Round 1 left R9 `unresolved` pending exactly these answers.
   Four correctable fields, a removal command and income corrections are plausibly more than one
   coherent change.
4. **The spelling of both commands**, under the delegation named above (`WI-0003/Q-004`), which
   round 1 wrote down in advance precisely so that spending it would be visible.

---

# Round 2

Held 2026-09-11, against the five answers `answer-questions` had propagated. The stakeholder is
not in this session (`SIMULATION-NOTICE.md`), so this round decided what the record and their
standing licences allowed, and filed the rest.

## Definition of Ready — round 2's walk

| # | Verdict | Why |
|---|---------|-----|
| R1 | pass | frontmatter complete; `depends-on` added this round |
| R2 | pass | unchanged from round 1 |
| R3 | pass | fifteen criteria, `AC1`–`AC15`, each a checkbox |
| R4 | **pass for what this round covers, fail overall** | AC1–AC15 each name a line to type and an outcome to observe; `## How each criterion is decided` below states the command and the verdict for every one of them. What fails is not a written criterion but a missing one: income is in this item's scope by `Q-005` and has no criterion, because `Q-006` and `Q-007` are open. R4 is recorded as failing, and the honest reading is that the fifteen written criteria are decidable and the sixteenth cannot be written yet |
| R5 | pass | five exclusions, and two of them — correcting a move, and the reference itself — are things a reader would reasonably assume were included |
| R6 | **fail by construction** | `Q-006`, `Q-007` and `Q-008` are open and blocking. This is the criterion that fails *because* refinement is in progress, and it is what suspends the item |
| R7 | pass | `depends-on: WI-0002, WI-0006` recorded, and the item is sequenced after both. `WI-0002` is `done`; `WI-0006` is not, and the dependency is what makes the order explicit rather than hoped for |
| R8 | **fail** | this file declares `status: agenda`, which is the truth while three questions are open |
| R9 | **resolved: not split** | round 1 left this `unresolved` pending the answers. With the reference moved to `WI-0006`, this item is `envel fix` and `envel remove` over one piece of machinery — locate an entry by its reference, change or drop it, re-check the one balance invariant. Splitting them would put that invariant in two items and make the second one unable to be verified without the first |
| R10 | **pass** | the combinations are AC6 (the four options in any combination, and none of them), AC5 with AC9 (a change of envelope that would take the destination below zero), AC3 with AC8 (a change of date that moves the spend between months), AC13 (a reference naming a move), AC1 and AC12 (a reference naming nothing). The one combination with no criterion — any option applied to an **income** — is named in `## Out of scope` as out *this round* and in `## Notes` with the two open questions that own it, which is what R10 asks for: visible, with who left it so |
| R11 | pass | no criterion on this item counts anything. AC15 names the criteria it checks rather than counting refusals |
| R12 | **pass, and one licence spent** | the command surface is `[assumed]` under `WI-0003/Q-004`, with the category written on the entry below. One further assumption is taken under **no** licence — AC4's empty description — and says so, with where a disagreement lands |

## Decided this round, and by what authority

- **`envel fix <ref>` and `envel remove <ref>`, with the reference as a plain word and each
  correctable field as a named option.** `[assumed]`.
  **Under delegation:** `WI-0003/Q-004` — argument style and the naming of commands and options:
  *"I'd rather everything in this tool be typed the same way than have one command that's
  special."* The licence is spent this way: the argument a command always takes is a plain word,
  as `envel spend` takes its envelope and `envel summary` its month; the ones it takes rarely are
  named options, as `--on` already is. A correction rarely changes more than one of four fields, so
  each field is an option. If the stakeholder dislikes a name, it costs one amendment to a
  criterion and no design.
  - The removal command is called `remove` rather than the `unspend` that appeared in
    `Q-003`'s option B. They endorsed the behaviour of that option, not the word, and `remove`
    survives whichever way `Q-007` goes — `unspend` would have to be renamed the moment an income
    could be removed. `Q-007`'s context puts the word in front of them, so the choice is visible
    rather than buried here.
- **A description can be removed by correcting it to an empty one** (AC4). `[assumed]`, under
  **no** delegation. The basis is `Q-002`'s own `## Cross-answer check`, which told the
  stakeholder that *"whether you can take one off again is part of the same answer and we will
  write it into the criteria whichever way you answer, rather than filing a sixth question about
  it."* That is a promise this round is keeping rather than a licence they granted. If they
  disagree, the disagreement lands on AC4 and costs one amendment; nothing else depends on it.
- **The reference belongs to `WI-0006`, and this item depends on it.** Not a licence but a reading
  of their own sentence at `Q-001`: *"That does mean the listing command has to exist, and I am
  saying yes to that separately."* Round 1's draft had this item creating the reference and
  `WI-0006` displaying it, which made the pair circular. If they had meant the reference to come
  first and the listing later, they would have chosen option D at `Q-001`, which is exactly that.
- **Not routed to `plan`, again.** Every open choice on this item is a line the stakeholder types
  or a message they read.

## Questions put to the stakeholder — round 2

Filed as `questions/Q-006.md`, `Q-007.md` and `Q-008.md`, all `addressed-to: human`, all
blocking, all open. One conversation in three artifacts: each `## Context` carries the *"round 2,
question N of 3"* frame and `Q-008` closes it (`spec/question.md` §2, F-020).

1. **Q-006 — which parts of an income can be corrected?** This is a cross-answer question and is
   filed as one. `WI-0005/Q-005` says corrections reach income *"in the same way as a spend"*;
   `WI-0003/Q-003` declined to give income a date at all — *"I'm not paying for rework on a
   command that already works for a case I don't have."* A spend's date is one of the four things
   `Q-002` made correctable, so *the same way* cannot be delivered without overturning the second
   sentence. Both are quoted verbatim and by ID and the stakeholder is asked which wins. ADR-0008
   §3 gives two moves and reconciling them here is not one of them.
2. **Q-007 — can an income be removed as well as corrected?** `Q-003` asked about a spend and the
   reply names a shop; `Q-005` extended correcting and was silent on removing. Removing an income
   is also the first thing in this tool that would move a balance **down** without being a spend,
   which their `WI-0001/Q-001` answer is watchful about.
3. **Q-008 — is the reference numbered within an envelope or across everything?** `Q-001`'s
   example showed a per-envelope `7`; `WI-0006/Q-003`, answered afterwards, asks for a listing with
   no envelope named, where a per-envelope number is ambiguous. It changes what they type on every
   correction.

None of the three is a question `refine` could have answered. Two are scope on their own data and
the third is what they type.

## Cross-answer check — round 2

`scripts/lint-answers --item WI-0005` passes, and the read it cannot make is this: one conflict
was found between two of the stakeholder's own answers, and it was filed rather than reconciled —
`WI-0005/Q-005` against `WI-0003/Q-003`, as `Q-006`. Nothing under `docs/` sourced to either
sentence was edited; the criteria this round wrote are about a spend, and the income criteria are
not written at all rather than written to one reading.

`Q-007` and `Q-008` are gaps rather than conflicts: in each, one answer is silent where the other
speaks, and no sentence of theirs has to lose.

## How each criterion is decided

The `criteria-are-decidable` gate, criterion by criterion. Every one is observed in a store of its
own — `ENVEL_FILE` pointing at a path that does not exist [src: ADR-0003] — set up with `envel
new`, `envel add` and `envel spend`, and read back with `envel list`, `envel summary` and the
listing of `WI-0006`.

| AC | Run this | Verdict |
|----|----------|---------|
| AC1 | `envel fix 999 --amount 1` against a store with no entry 999 | stderr names `999`, exit non-zero, `envel list` byte-identical before and after |
| AC2 | `envel fix <ref> --amount 14.00` on a spend of 12.50 | stdout names the envelope and its new balance, exit 0; `envel list` shows the envelope 1.50 lower |
| AC3 | `envel fix <ref> --on 2026-08-28`, then `--on 7/9`, then `--on <tomorrow>` | the first succeeds; the second and third write to stderr and exit non-zero with nothing changed |
| AC4 | `envel fix <ref> --description "lunch"`, then `--description ""` | the store's entry gains `lunch`, then carries no description key at all |
| AC5 | `envel fix <ref> --envelope "eating out"`, then `--envelope nosuch` | the first moves the amount between the two envelopes in `envel list` and leaves a third alone; the second writes to stderr and exits non-zero |
| AC6 | `envel fix <ref>` with all four options, then with none | the first applies all four; the second prints the subcommand's usage to stderr and exits non-zero |
| AC7 | `envel list` before and after a correction | only the envelopes named by the correction differ, and by exactly the corrected amounts |
| AC8 | `envel summary 2026-08` and `envel summary 2026-09` around a correction that changes a date | the spend's amount appears in exactly one of the two, the month of its date after the correction |
| AC9 | `envel fix <ref> --amount 140.00` where the envelope holds 30.00 | stderr names the envelope, `30.00` and `110.00` short; exit non-zero; `envel list` unchanged |
| AC10 | `envel fix <ref> --amount 0` and `--amount -5` | each writes to stderr, exits non-zero, changes nothing |
| AC11 | `envel remove <ref>` on a spend | stdout names the envelope, the date and the amount removed and the new balance; exit 0; no prompt is written and no input is read |
| AC12 | `envel remove 999` | stderr names `999`, exit non-zero, nothing changed |
| AC13 | `envel fix <ref>` and `envel remove <ref>` on the reference of a move entry | each writes a message to stderr saying a move cannot be corrected or removed, exits non-zero, changes nothing |
| AC14 | any correction, then a separate invocation of `envel list` and `envel summary` | the corrected figures are there |
| AC15 | the cases named in AC15 itself | each refusal on stderr with a non-zero exit; each success on stdout with exit 0 |

## What round 2 leaves for round 3

All three replies have now arrived and `answer-questions` has propagated them; the item returns
to `draft`. What round 3 inherits:

1. `Q-006` and `Q-007` are answered and the income criteria are written — AC16 for correcting,
   AC17 for removing, AC18 carrying `Q-004`'s below-zero rule to both. Round 3 walks the
   Definition of Ready against them: R4 has to find each decidable, and R10 has to say what the
   combinations of an income reference with AC2 to AC6's options are, now that two of those four
   options are refused on one.
2. `Q-008` is answered and AC1 says what a reference looks like. The answer lands on `WI-0006` as
   well, which is where the reference is created and printed; `item.md`'s `## Notes` carries what
   `WI-0006`'s own round 2 has to write, because this item cannot edit a sibling's criteria.
3. R8 set to `recorded`, once the exchange is a finished conversation.
4. `## How each criterion is decided` extended to AC16, AC17 and AC18 — the table stops at AC15,
   and three criteria without a row in it are three criteria the `criteria-are-decidable` gate has
   not been shown.

## Answers — round 2

Received 2026-09-11, all three, verbatim. Consumed by `answer-questions`
(`questions/Q-006.md`, `Q-007.md`, `Q-008.md`, each `status: answered`, `answered-by: human`).

**Q-006 — which parts of an income can be corrected?** → **B**, the amount and the envelope.

> [human] B — the amount and the envelope. What I meant by "the same way as a spend" was that
> anything I can type wrong when I put it in, I can put right; income has two of those and a spend
> has four, and that is the whole of the difference. I am not giving income a date by the back
> door after turning it down two rounds ago, and I am not leaving a dated-income item sitting on
> the board either — that is D and it is a nice-to-have, not this round. If a payslip in the wrong
> month ever actually costs me something I will come and tell you, as I said before.

**Q-007 — can an income be removed as well as corrected?** → **B**, spends and income, one
command, no flag.

> [human] B — spends and income, one command. You are right that my reason was the duplicate, not
> the shop: a payslip entered twice is money I do not have sitting in an envelope, and inventing a
> fake spend to cancel it would be worse than the mistake. What I said about not wiping money out
> by accident was about an envelope disappearing under me, not about me removing an entry I asked
> it to remove — the command telling me what it took out is enough. No flag.

**Q-008 — is the reference per-envelope or global?** → **A**, one number across everything.

> [human] A — one number across everything. The 7 in my round-1 answer was your example, not my
> decision; what I care about is copying one thing off the line in front of me and typing it back.
> Three-figure numbers do not bother me — I am reading them off the screen, not remembering them —
> and I am not learning a slash.

## Cross-answer check — round 2, on the replies

Written on each question file as it was consumed; collected here so a reader of this item's
refinement story passes through it. The full per-ID verdicts are in the `## Cross-answer check`
section of each question.

- **No conflict was found**, on any of the three. The pair round 2 filed `Q-006` *for* —
  `WI-0005/Q-005` (*"in the same way as a spend"*) against `WI-0003/Q-003` (income takes no date)
  — was settled **by the stakeholder**, in favour of the older sentence, with their own reading of
  what *the same way* had meant. That is ADR-0008 §3's intended outcome, and it is why round 2
  filed the question rather than reconciling the two sentences itself.
- The reply to `Q-007` reads `WI-0001/Q-001` — *"nothing should ever be able to wipe money out of
  an envelope by accident"* — for us, and narrows it to the case it was about. Nothing under
  `docs/` sourced to that answer was edited: the sentence still says what it said, and the
  narrowing is recorded as their statement rather than as a repair.
- The reply to `Q-008` retires the per-envelope `7` that appeared in `Q-001`'s reply, and the
  stakeholder says in terms that the `7` was our example rather than their decision. `Q-001`'s
  answer is therefore not overtaken: what it decided — a short printed reference, read off a
  listing — stands unchanged, and `Q-008` decides only what the number counts.
- The reply to `Q-006` declines to file the dated-income item that option D offered. No work item
  was created, and `## Out of scope` in `item.md` records the refusal in their words rather than
  leaving the gap silent.

---

# Round 3

Held 2026-09-11, against both sets of answers, all of them propagated. This is the round that
reaches Ready. It put **no** question to the stakeholder, and the reasoning for that is below
rather than left as a silence.

## Definition of Ready — round 3's walk

| # | Verdict | Why |
|---|---------|-----|
| R1 | pass | `item.md` frontmatter is complete; `type: work-item`, `epic: EP-001`, `priority: medium`, and `depends-on` names `WI-0002` and `WI-0006`. `scripts/validate-workspace` agrees — 0 errors, 0 warnings |
| R2 | pass | `## Story` names the role (a person budgeting their own money at a terminal), the capability (correct a spend already recorded) and the outcome (*"so that a mistyped amount does not stay in my figures and a summary I look at later shows what I actually spent"*). Unchanged since round 1 |
| R3 | pass | twenty criteria, `AC1`–`AC20`, each a checkbox |
| R4 | **pass** | this is the criterion round 2 recorded as failing, and what was failing was a missing criterion rather than a written one: income was in scope by `Q-005` and had none. `Q-006` and `Q-007` are answered and AC16, AC17 and AC18 are written; `## How each criterion is decided — round 3` below names the command and the verdict for every one of AC16 to AC20, and round 2's table does the same for AC1 to AC15. No criterion carries an adjective without a threshold; the nearest thing to one is AC1's *"short"*, which is the stakeholder's own word about a number whose form AC1 then fixes — one number counted once across everything recorded |
| R5 | pass | eight exclusions. Three of them are things a reader would reasonably assume were included: correcting a move, changing what kind an entry is, and undoing a correction. The last two are round 3's, and the kind bullet says in terms that it is `refine`'s decision and not the stakeholder's |
| R6 | **pass** | no question on this item is open. All eight — `Q-001` to `Q-008` — are `status: answered`, `answered-by: human`. This is the criterion that failed by construction in rounds 1 and 2 and it clears because the conversation finished, not because anything was waived |
| R7 | **pass** | `depends-on: WI-0002, WI-0006`, and both are `done`. In round 2 this passed on the weaker reading — the dependency recorded and the item sequenced after it — because `WI-0006` was not built. It now passes on the stronger one: nothing in `depends-on` is unfinished |
| R8 | **pass** | this file declares `status: recorded`, and the exchange above it is the whole conversation: eight questions, eight answers verbatim, every one tagged, nothing `[unresolved]` |
| R9 | **pass — not split**, as round 2 resolved it | the reference belongs to `WI-0006`, which is built. What is left here is `envel fix` and `envel remove` over one piece of machinery — locate an entry by its reference, change or drop it, re-check the one balance invariant. Splitting them would put that invariant in two items and make the second unverifiable without the first. Round 3 re-read this against the income criteria that arrived since, and they do not change it: AC16 and AC17 reach the same machinery with a narrower set of fields |
| R10 | **pass** | the combinations are enumerated below, and the two that had no criterion when round 3 started now have AC19 and AC20 |
| R11 | pass | no criterion on this item counts anything it may move. AC15 and AC19 name the criteria they range over rather than counting them, and AC20 names the lines it constrains. The one number round 3 wrote down — the `-42.30` opening figure in `## Notes` — was measured before it was written and carries the command and its outcome as a citation |
| R12 | **pass, and the licences named** | one standing delegation is spent on this item — `WI-0003/Q-004`, for the command surface — and it carries its `**Under delegation:**` line at the head of the criteria. Three assumptions are taken under **no** licence and each says so where it is made: AC4's empty description (round 2), AC19's all-or-nothing refusal and AC20's listing (round 3). `scripts/lint-answers --item WI-0005` passes |

## R10 — every combination this item introduces, and where each one is settled

The behaviours are two subcommands, four options on one of them, and three kinds of entry a
reference can name. The product is small enough to state outright.

| Combination | Where it is settled |
|-------------|---------------------|
| `fix` with each of `--amount`, `--on`, `--description`, `--envelope` on a **spend** | AC2, AC3, AC4, AC5 |
| `fix` with any two, three or four of them at once on a spend | AC6, with the worked four-option example |
| `fix` with none of them | AC6 — the subcommand's usage on stderr, non-zero, nothing changed |
| `fix --amount` or `--envelope` on an **income** | AC16, behaving as AC2 and AC5 do on a spend |
| `fix --on` or `--description` on an income | AC16 — refused, naming what an income does not carry |
| `fix` on an income with an accepted option and a refused one in the same invocation | **AC19** — the whole invocation is refused and nothing is applied. This is the combination round 3 found missing |
| `fix` or `remove` on a **move** | AC13 — refused. Both halves of a move are `kind: "move"` entries with their own references [src: ADR-0007], so either number is refused |
| `fix` or `remove` on a reference no entry has | AC1, AC12 |
| `--envelope` naming an envelope that does not exist | AC5, and on an income through AC16 |
| `--envelope` taking the destination below zero, on a spend | AC5 with AC9 |
| `--envelope` taking the source below zero, on an income | **AC18**, which round 3 widened: it is the one income correction that goes below zero with no figure reduced |
| `--amount 0` or a negative `--amount`, on either kind | AC10, restated for income at the end of AC16 |
| `--on` moving a spend between months | AC3 with AC8 — it leaves one month's summary and appears in exactly one other |
| `remove` on a spend, on an income | AC11, AC17 — one subcommand, no flag, nothing asked before acting |
| `remove` of an income that would leave an envelope short | AC18 |
| any of the above, then reading `envel entries` | **AC20** — the listing the reference was read off shows the change. The second combination round 3 found missing |
| any of the above, then a separate invocation | AC14 |
| every refusal's stream and exit code, every success's | AC15, which lists the criteria it ranges over |

Three combinations are deliberately unconstrained, and this is where R10 asks them to be visible:

- **A correction that changes nothing** — `envel fix 7 --amount 12.50` where the amount is already
  `12.50`. It succeeds and prints, by AC2; nothing says it must notice. Left so by `refine`.
- **`--envelope` naming the envelope the entry is already in.** The same case; AC5's arithmetic is
  a no-op and the criterion holds trivially. Left so by `refine`.
- **`--on` setting a date before the envelope existed.** The delivered `envel spend` refuses only
  a future date [src: WI-0002 AC12 "that is later than today is refused with a message saying the date is in the future"],
  so AC3 inherits exactly that and no more. Left so by `refine`, consistent with what is built.

## Decided this round, and by what authority

Two decisions, both written as criteria, both `[assumed]` under **no** delegation, each naming
where a disagreement lands. They are recorded here as well as on the criteria because R12's point
is that a licence spent silently is a decision taken on someone's behalf with no way back.

- **A refused `envel fix` applies none of itself** (AC19). `[assumed]`, under **no** delegation.
  The basis is not a licence but the tool's own delivered behaviour, in the words the stakeholder
  reads: every refusal in `envel/envelopes.py` ends *"Nothing has been changed."*, *"Nothing has
  been recorded."* or *"Nothing has been moved."*, and the stakeholder has never asked for a
  command that does part of what it was told. The alternative — apply what is acceptable, refuse
  the rest, report both — is a real design and it is the one this criterion rules out. If they
  want it, the disagreement lands on AC19 and AC6 and costs one amendment to each.
- **`envel entries` shows the change** (AC20). `[assumed]`, under **no** delegation. Nobody has
  said the listing must reflect a correction, and it plainly must: it is the listing the reference
  is read off [src: WI-0005/Q-001], so a listing that did not would hand the stakeholder a number
  for an entry that no longer says what the line says. Written as a criterion rather than left to
  `implement` because it is the only place the two items meet after `WI-0006` closed.

And one thing round 3 **did not** decide, recorded because deciding it would have been easy:

- **Whether the below-zero rule reaches `envel entries`' opening figure.** It does not, and
  `## Notes` in `item.md` says so with the measurement behind it. That is a statement about what
  AC9 and AC18 already mean, not a new rule — and the negative opening figure it describes is a
  consequence of two decisions the stakeholder has already taken and already been told the cost
  of [src: WI-0003/Q-003]. `refine` does not evaluate delivered behaviour, so nothing was filed
  against `WI-0006`; what was done is to write down which figure the criteria are about, so that
  `implement` does not invent a second check.

## Why round 3 put nothing to the stakeholder

`refine` step 3, applied to every gap round 3 found. None of them reached the first test — an
answer that changes what the software is *for*, what it promises, or what they would notice in a
way they have not already been asked about:

- **AC19** is a convention they see in every refusal message the tool already prints. Asking would
  be asking them to reaffirm the thing eight delivered criteria already do.
- **AC20** is not a choice. A listing that did not show a correction would contradict `Q-001`'s
  answer, which is the reason the listing exists.
- **AC18's widening** applies `Q-004`'s own sentence — *"No negative envelopes anywhere in this
  tool, and that includes here"* — to a third route to the same place. Their answer already covers
  it in terms; narrowing it to two of three routes would have been the decision, not widening it.
- **The three unconstrained combinations** above are each a case where doing nothing special is
  what the delivered commands already do.

Nothing was routed to `plan` this round either, for the reason rounds 1 and 2 both gave: every
open choice on this item is a line the stakeholder types or a message they read.

## Cross-answer check — round 3

`Checked against: WI-0005/Q-001, Q-002, Q-003, Q-004, Q-005, Q-006, Q-007, Q-008, WI-0001/Q-001,
WI-0001/Q-003, WI-0002/Q-001, WI-0003/Q-003, WI-0003/Q-004, WI-0004/Q-001, WI-0006/Q-001,
WI-0006/Q-003, EP-001/Q-002, EP-001/Q-003, EP-001/Q-005.`

**No conflict was found, and no answer of theirs was edited.** Round 3 recorded no new answer, so
what it checked is each criterion it wrote or amended against the answers it rests on:

- **AC19** against `EP-001/Q-002` (an overspend is refused rather than shown) and `WI-0005/Q-004`
  (*"Doing it in two steps is fine; seeing a minus number is not"*). Both are the stakeholder
  choosing a refusal over a half-measure, which is what AC19 generalises. Neither says anything
  about an invocation carrying several changes, so AC19 adds to their answers rather than
  reinterpreting one.
- **AC20** against `WI-0005/Q-001` and `WI-0006/Q-003`. `Q-001` makes the listing the source of
  the reference and `Q-003` makes the envelope optional on it; AC20 asks only that what those two
  answers produce stays true after a correction. `EP-001/Q-003` — *"I definitely don't want every
  individual spend listed"* — is about the monthly summary and is untouched: AC20 names
  `envel entries`, which they asked for separately and by name.
- **AC18's widening** against `WI-0005/Q-004` and `WI-0005/Q-006`. `Q-004` gives the rule for the
  whole tool; `Q-006` gives `--envelope` on an income its meaning. The widening is the two read
  together, and neither has to lose.
- **The stale citations round 3 repaired** were false because the *code* moved under them —
  `WI-0006` added the reference counter and shifted `add_income` down eleven lines — not because
  the stakeholder has since said something else. That is the ordinary repair `refine` is allowed
  to make, and it is deliberately recorded as distinct from the one it is not (ADR-0008 §3).
- **The `WI-0006` obligations** round 2 wrote into `## Notes` were discharged by `WI-0006`'s own
  round 3, not by this item editing a sibling. The notes now say so and cite `WI-0006` AC3 and AC4.

The read `scripts/lint-answers` cannot make, stated for the reader: the one pair of the
stakeholder's own sentences that ever collided on this item — `WI-0005/Q-005` against
`WI-0003/Q-003` — was put to them as `Q-006` and settled by them in favour of the older sentence.
Round 3 did not reopen it and wrote no criterion that depends on the newer reading.

## How each criterion is decided — round 3

Round 2's table above covers AC1 to AC15 and still holds; `--description` on a `fix` is a named
option while the delivered `envel spend` takes its description as a trailing word, which is the
delegation at `WI-0003/Q-004` spent as the head of `## Acceptance criteria` describes it — a
command's usual argument is a plain word and its rare ones are named options, and a correction
rarely touches a description
[src: run: python3 -m envel spend groceries 12.50 shop → exit 0, `spent 12.50 from groceries, which now holds 87.50`].

The five criteria round 2 and round 3 added:

| AC | Run this | Verdict |
|----|----------|---------|
| AC16 | on an income's reference: `envel fix <ref> --amount 80.00`, then `--envelope "eating out"`, then `--on 2026-09-01`, then `--description x` | the first two succeed and move the figures `envel list` shows; the last two each write to stderr, exit non-zero, and leave `envel entries` printing the same line as before |
| AC17 | `envel remove <ref>` on an income's reference | stdout names the envelope and the amount removed and what the envelope holds afterwards; exit 0; no input is read; `envel list` shows that envelope lower by the amount |
| AC18 | an envelope holding 100.00 of income with 90.00 of spends against it: `envel remove <income-ref>`, then `envel fix <income-ref> --amount 50.00`, then `envel fix <income-ref> --envelope "eating out"` | each writes to stderr naming the envelope, `100.00` and how short the change leaves it; each exits non-zero; `envel list` is identical after all three |
| AC19 | `envel fix <income-ref> --amount 20.00 --on 2026-09-01` | stderr, non-zero, and the line `envel entries` prints for `<ref>` is byte-identical before and after, as is `envel list` |
| AC20 | `envel entries --month <m>` before and after each of a `--amount` fix, an `--on` fix into another month, an `--envelope` fix and a `remove` | the reference's line carries the new amount; leaves month `<m>` and appears once in the new month; names the new envelope; is absent from every month. With an envelope named, the opening figure plus the lines between equals the closing figure in each case |
