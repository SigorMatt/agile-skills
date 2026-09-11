# Journal — WI-0004

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-09-11T02:14:53Z — answer-questions v0.6.3 — architect

- **Item:** WI-0004
- **Trigger:** created by `answer-questions` while consuming the stakeholder's answers on `EP-001`; this item did not exist before that answer
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-005.md` — the stakeholder's answer, option C: *"Moving money between envelopes is normal practice and I will need it the moment an envelope runs short, which is the same week I start using this."*
  - `tracker/items/EP-001/questions/Q-002.md` — the overspend answer, which is what makes a move the stakeholder's chosen route when a spend is refused
  - `tracker/items/EP-001/questions/Q-006.md` — the command's name, `envel`, so AC1 can say what to type
  - `tracker/items/EP-001/item.md` — the epic's scope, which this item is now part of
  - `tracker/items/WI-0001/item.md` and `tracker/items/WI-0002/item.md` — the existing items, to confirm this work belongs in neither
  - `.claude/agile-skills/spec/ids-and-statuses.md` §5 — the creation authority under which this item was filed
- **Decisions:**
  - **Filed as its own work item rather than folded into `WI-0001` or `WI-0002`.** `answer-questions` step 3b: an answer that implies work no item records is filed as a `work-item` at `draft` with `arose-from` naming the question. Widening an existing item to swallow it would have hidden the scope change from the board and from the person who asked for it.
  - **Two items, not one.** `EP-001/Q-005` option C is two capabilities — moving money and correcting an entry — with different criteria and different unknowns. `WI-0005` is the other one. One item covering both would be refined and verified as a bundle.
  - **`depends-on` deliberately not recorded yet.** The dependency on `WI-0001` is real, but `pipeline.yaml`'s `runnable` rule gates every dispatch on `depends-on` being `done`, which would freeze this item's own refinement until `WI-0001` is delivered. It is written in `## Notes` instead, for `refine` to record when it has asked its questions.
  - **The criteria are a draft, and the item says so.** Three things this item needs are named in `## Notes` as `refine`'s to ask, including whether a move appears in the monthly summary — `EP-001/Q-003` settled the summary's columns before this item existed.
- **Questions raised:** none — the open points are recorded in `## Notes` for `refine`, which talks to the stakeholder directly
- **Commands:**
  - `.claude/agile-skills/scripts/new-item --id WI-0004 --type work-item --title "Move money between envelopes" --epic EP-001 --priority medium --status draft --actor answer-questions --arose-from EP-001/Q-005` → exit 0, created at `draft`
- **Gates:**
  - `answer-is-propagated` → **pass** (this item **is** part of the propagation of `EP-001/Q-005`; it is named in that question's `## Consequences` and it exists)
  - `answered-from-the-record` → **pass** (the basis is the stakeholder's own `## Answer` on `EP-001/Q-005`, quoted above and in `## Notes`)
  - `escalation-is-justified` → **skipped** (nothing was escalated from this item)
  - `propagated-claims-carry-their-obligation` → **pass** (this execution wrote nothing under `docs/` from this item; the claims it wrote are acceptance criteria in `item.md`)
  - `engagement-state-is-left-to-the-ending` → **pass** (no `## Engagement state` section was written or amended here)
  - `cross-answer-consistency` → **pass** (the cross-answer check for `EP-001/Q-005` is written on that question and in `EP-001`'s journal, where the answer was consumed)
  - `workspace-valid` → **pass** (`validate-workspace` run at the end of the `EP-001` execution this item was created by)
  - `item-resumed-correctly` → **skipped** (this item was created, not resumed; its history has one row and no `resume-to`)
  - `a-deferral-is-not-an-answer` → **skipped** (no reply on this engagement deferred)
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` (new) — story, five acceptance criteria, three exclusions, and the open points `refine` must ask about
  - `tracker/items/WI-0004/history.md`, `tracker/items/WI-0004/journal.md` (new, by `new-item`)
- **Status:** `—` → `draft`
- **Result:** `WI-0004` exists at `draft` because the stakeholder asked for moving money between envelopes at `EP-001/Q-005`. It is not Ready and has not been refined; what it still needs is written in its `## Notes`.

## 2026-09-11T05:13:15Z — refine v0.6.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** `draft` — dispatched by `next` as the highest-ranked runnable item. Step 4 of the orchestrator sits above the halt, so `WI-0003`'s two open human questions did not stop this item running. Among the runnable drafts `WI-0004` and `WI-0005` tie at priority rank 3 and this one has the earlier `created` (02:12:40Z against 02:12:52Z); `WI-0006` is rank 4.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the story, five draft criteria, three exclusions, and the three open points the draft named as `refine`'s to ask about
  - `tracker/items/WI-0004/history.md` — **read first, as the procedure requires.** One row, `— → draft`, actor `answer-questions`. This is a **fresh draft**, not a send-back, so round 1 is a first refinement and there is no named defect to scope it
  - `tracker/items/WI-0004/journal.md` — `answer-questions`' creation entry, which records why the item was filed separately, why `depends-on` was withheld, and that the criteria are a draft
  - `tracker/items/EP-001/questions/Q-005.md` — the answer this item arose from, in full
  - `tracker/items/EP-001/questions/Q-002.md` and `Q-003.md` — the overspend rule that makes a move the stakeholder's chosen route, and what the summary shows
  - `tracker/items/WI-0002/questions/Q-001.md` and `Q-002.md` — a spend's date and its optional description, both in the stakeholder's own words
  - `tracker/items/WI-0003/questions/Q-001.md` and `Q-003.md` — **the two that changed this round.** `Q-001` already answers the draft's first open point; `Q-003` is the answer that makes the date question genuinely open rather than derivable
  - `tracker/items/WI-0001/questions/Q-003.md` — zero and negative income refused, the rule the third open point asked about
  - `tracker/items/WI-0003/item.md` — AC2, AC3 and AC6 as they now stand, which are the constraints this item has to be recordable against
  - `tracker/items/WI-0001/item.md` and `tracker/items/WI-0002/item.md` — the delivered command surface and the conventions AC-writing will cite
  - `tracker/items/WI-0006/item.md` — its scope, which is what decides the description question
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md` §2, `spec/doc-header.md` §4a
- **Decisions:**
  - **One blocking question filed, and only one.** `WI-0004/Q-001` — is a move datable the way a spend is, or always dated when it is typed, the way income is? It is filed because the stakeholder has answered this shape of question **twice, with opposite answers**, each reasoned from their own habits with a particular kind of event: `WI-0002/Q-001` (a spend can be back-dated, *"I will not always sit down with the receipts on the day"*) and `WI-0003/Q-003` (income cannot, *"I put income in when it arrives"*). A move is a third kind of event and neither answer reaches it; picking a precedent would be deciding which of their habits this one resembles. It is not cosmetic: `WI-0003` AC2's fourth column is per month, so the date decides which report a move lands in, and under the no-date options a move in the wrong month cannot be repaired at all, because `WI-0005` is scoped to spends.
  - **The draft's first open point was already answered and was not re-asked.** It asked whether a move appears in the summary as money in and money out. `WI-0003/Q-001`, answered after this item was filed, settles exactly that: option C, a move is kept out of *spent* and shown as its own net figure. What it leaves here is a pair of **constraints** on how a move is recorded, routed to `plan`, not a question.
  - **The draft's second open point was split, and the halves went opposite ways.** The date is `Q-001`. The description is decided: **a move carries none**, `[assumed]` under no delegation, because nothing in this project would ever show one back — `WI-0006` is scoped to the spends recorded against an envelope, and `EP-001/Q-003` ruled the individual entries out of the summary. It is deliberately not read as contradicting `WI-0002/Q-002`, where they asked for an optional description on a **spend** and gave a reason — *"the ones I might query later"* — that presupposes something that queries. Because it is a scope decision rather than a detail, it went into `## Out of scope` as well as `## Notes`, and `Q-001` names it to the stakeholder in as many words so the decision reaches them in the same breath as the question.
  - **The draft's third open point was decided rather than asked.** Zero or a negative amount is refused. `[assumed]`, under no delegation: the stakeholder set the rule once for income at `WI-0001/Q-003`, `WI-0002` AC6 took it for a spend on the same footing and it has shipped and been verified, and asking about the third instance of a rule they stated once would tell them their answer was not heard.
  - **Two further things decided under no delegation**, both on the same footing as every other word below `envel`: the subcommand is `move`, as `envel move <from> <to> <amount>`, source first and amount last, which is the order both delivered subcommands already use and the order the story reads in; and a move to and from the same envelope is refused. The real risk in the first is reversing the pair and moving money the wrong way, which succeeds where a refusal would not — mitigated in the criteria rather than by a question, by requiring the success line to name which envelope the money left and which it arrived in.
  - **`depends-on: WI-0001` recorded, which is the R7 failure.** The draft withheld it on the ground that the `runnable` rule would freeze this item's own refinement until `WI-0001` was delivered. That reason has expired — `WI-0001` is `done` — so recording it now costs nothing. `WI-0002` is **not** a dependency: moving money needs envelopes, not spending, and no criterion here is written against anything `WI-0002` delivers.
  - **One `## Out of scope` entry contradicted itself and was rewritten rather than deleted.** It deferred correcting a move to `WI-0005` *"which the stakeholder scoped to spends"* — deferring to an item it says in the same sentence does not cover it. The gap is real: nothing in this epic repairs a move. Round 1 leaves the gap and says so, because a move is self-reversing and `WI-0003`'s fourth figure is a **net** number, so a mistake and its reversal cancel in the only place a move is ever displayed. What does not cancel is the month each lands in, which is why that cost is stated inside `Q-001`'s options rather than left to be discovered.
  - **No acceptance criterion was rewritten.** AC1 is downstream of `Q-001` — whether the line carries `--on` is the question — and the five criteria round 1 could already write would have to be numbered around it. Round 2 writes them once from the reply.
  - **Three design questions routed to `plan`**, none of them new to this engagement: how a move is stored and how `WI-0003` tells it from a spend and from income; the order the refusals are checked in; and what happens to an entry naming an envelope that is no longer present. The last two are the same questions `WI-0002` and `WI-0003` routed there, and the note says they should get the same answer.
- **Questions raised:** one, blocking, addressed to `human` — `WI-0004/Q-001`. Full text in the question file; the round's record is `artifacts/refinement-qa.md`. None left `[unresolved]`.
- **Commands:**
  - `grep -rn 'WI-0004 AC' tracker docs` → exit 0, one line, and it is `item.md` quoting the command itself inside backticks — a mention rather than a citation (`spec/doc-header.md` §4a), so nothing anywhere cites this item's criteria by number
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0004` → exit 0, 0 consumed human answers, 0 delegations
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 after the transition; before it, the two errors this round's own act creates — `board.stale` and `question.blocking.not-suspended` on an item still at `draft`
- **Gates:**
  - `workspace-valid` → **pass** — `validate-workspace .` → exit 0. Filing a blocking question against an item still at `draft` raises `question.blocking.not-suspended` by construction; the suspension this transition makes is what clears it, which is why the gate is read after the move rather than before it. Every citation written this round resolves, including the four anchored criterion citations into `WI-0001`, `WI-0002` and `WI-0003`.
  - `definition-of-ready` → **fail, criterion by criterion.** R1 pass (frontmatter complete; `type`, `epic`, `priority`, `arose-from` set). R2 pass (`## Story` names role, capability and outcome, and the outcome is their own route out of a refused overspend). R3 pass (five labelled checkboxes). **R4 fail** — AC1 names no command surface, and five things the tool will certainly do have no criterion at all: what a successful move prints, which stream anything goes to, a zero or negative amount, a move to and from the same envelope, and the wrong number of words. `Q-001` blocks the first; round 2 writes the rest. R5 pass — and one entry was rewritten because it deferred to an item that does not cover it, plus a second entry added for the description decision. **R6 fail by this round's own act** — one blocking question now open, which is what suspends the item. **R7 closed this round** — `depends-on: WI-0001` recorded, and `WI-0001` is `done`. **R8 closed this round** — `artifacts/refinement-qa.md` written, `status: recorded`, carrying the whole round. R9 pass (one coherent change: one subcommand that reads the store, moves an amount and writes it back). **R10 fail** — a move's date has no stated behaviour pending `Q-001`; its description now does, in `## Out of scope` and `## Notes`, with who left it so. R11 pass (no criterion counts anything). **R12 pass** — four `[assumed]` decisions, every one saying in terms that it was taken under **no** delegation and naming where a disagreement lands; no standing licence exists in this engagement to spend, and none was claimed.
  - `criteria-are-decidable` → **fail on AC1, and the fail is R4's.** AC2 is settled by running the listing before and after a move and comparing three envelopes' lines. AC3 by attempting a move larger than the source holds and reading stderr, the exit code and the unchanged listing. AC4 by naming a non-existent envelope on each side in turn. AC5 by two separate invocations against one `ENVEL_FILE`. AC1 names no command to run — *"There is an `envel` command that moves a given amount"* — and until `Q-001` is answered nobody can write the invocation a verifier would type, because whether the line carries `--on` is the question. Recorded as failing rather than papered over with a plausible command line.
  - `cross-answer-consistency` → **pass** — `lint-answers --item WI-0004` → exit 0. This execution consumed **no** answer — round 1 asks, it does not propagate — so `Checked against: none`, with that reason. `Q-001` carries its `## Cross-answer check` filed **with** the question, naming `WI-0002/Q-001`, `WI-0003/Q-003`, `WI-0003/Q-001`, `EP-001/Q-002` and `EP-001/Q-005`. The watch on it is unusual and is written down: the two prior answers already point opposite ways, so whichever way the reply goes one will look like the precedent and the other will not, and **neither is overturned by either outcome** — a move is a third kind of event. The question says so explicitly, so the reply cannot be recorded as a reversal. If the stakeholder themselves frames it as changing one of those answers, that is an ADR-0008 §3 conflict and goes back to them quoting both.
  - `qa-recorded-verbatim` → **pass** — `artifacts/refinement-qa.md`, `status: recorded`, carries the DoR walk as a table, what became of each of the draft's three open points, the one question with why it is theirs, the four `[assumed]` decisions each with its **under no delegation** line and where a disagreement lands, the self-contradictory scope entry quoted before it was rewritten, the three items routed to `plan`, and what round 1 has not settled. No answer was received this round, so nothing is tagged `[human]` by it; every stakeholder sentence quoted is copied from the `## Answer` of the question named beside it.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-001.md` — new, blocking, to `human`
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — new, `status: recorded`
  - `tracker/items/WI-0004/item.md` — `depends-on: WI-0001` added; `## Out of scope` rewritten and extended; `## Notes` replaced. **No criterion changed, and no criterion changed its number.**
- **Status:** `draft` → `awaiting-answer`
- **Result:** `WI-0004` round 1 put one question to the stakeholder and settled everything else from the record. The question is the one thing here that cannot be derived: they have said a spend may be back-dated and that income may not, each for a reason about their own habits, and a move is a third kind of event that neither answer reaches — while the date decides which month a move appears in on `WI-0003`'s fourth column. Two of the three open points the draft listed did not survive: one was answered by `WI-0003/Q-001` after the draft was written, and the other two were decided here under no delegation and recorded where the stakeholder can see them. Round 2 writes AC1 from the reply, appends five criteria, and closes R4 and R10.

## 2026-09-11T05:22:31Z — answer-questions v0.6.3 — architect

- **Item:** WI-0004
- **Trigger:** `awaiting-answer` since `refine` round 1 suspended the item, with `resume-to: draft`
  on that history row. The stakeholder's reply had arrived in `Q-001`'s `## Answer` section, so the
  question was answerable in the precondition's sense and this skill is the only one that may
  consume it.
- **Inputs read:**
  - `tracker/items/WI-0004/questions/Q-001.md` — the only question ever filed on this item, with
    the reply, the three options and the cross-answer watch `refine` filed with it
  - `tracker/items/WI-0004/item.md` — the five criteria, `## Out of scope` and the whole of
    `## Notes`, including the four decisions round 1 took under no delegation
  - `tracker/items/WI-0004/history.md` — the suspending row and its `resume-to: draft`
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — round 1's agenda, what the draft asked
    `refine` to ask, the decisions and their authority, and `## What round 1 has not settled`
  - `tracker/items/WI-0004/artifacts/` — no `plan.md` exists; this item has never been planned, so
    there is no invalidation set for this execution to write into
  - `docs/architecture/adr/` — all six ADRs, checked for anything this answer would contradict.
    `ADR-0006` is the one that comes closest and it is titled *a spend carries the date it
    happened*, scoped to spends throughout; `ADR-0001` (integer cents), `ADR-0002` (JSON entry
    log), `ADR-0003` (store location), `ADR-0004` (invocation package and shim) and `ADR-0005`
    (stdlib-only checks) are untouched by a date on a move. No contradiction, so no escalation
    under `spec/question.md` §4's third condition.
  - `docs/product/vision.md` v2 — read in full, for whether this answer had to be propagated into
    it. Moving money is named there as something the stakeholder asked for; nothing in it states
    or implies when a move happened.
  - `tracker/items/WI-0002/item.md` — AC9, AC11 and AC12, the delivered spend date rules the three
    new criteria cite
  - `tracker/items/WI-0003/item.md` — AC2 and AC8, for what the answer changes about the summary's
    fourth column and for whether the income rule moved
- **Decisions:**
  - **Q-001 — answered by the human, route: escalation returned.** Option A: a move is datable
    exactly the way a spend is. Propagated into AC1 (the optional `--on <date>`, and the move held
    against the date given rather than the day typed) and into three appended criteria — AC6 (today
    by default, cited to `WI-0002` AC9), AC7 (`YYYY-MM-DD` and nothing else, cited to `WI-0002`
    AC11) and AC8 (a future date refused, today's own date accepted, cited to `WI-0002` AC12).
    Option A said *"all identical to `envel spend`"*, so the three are the delivered rules cited
    rather than three new decisions.
  - **Neither prior answer was recorded as overturned.** Round 1 filed the question saying that
    whichever way the reply went, one of `WI-0002/Q-001` and `WI-0003/Q-003` would look like the
    precedent and the other would not, and that neither was being reversed. The reply follows the
    spend rule, does not mention income, and does not frame itself as changing anything. `envel add`
    is untouched and `WI-0003` AC8 still says income is dated when it is typed.
  - **The `## Out of scope` correcting-a-move entry was amended rather than left.** It pointed at
    `Q-001` as the open thing that decided whether self-reversal was enough. With `--on` available,
    a reversal can be dated into the month the mistake landed in, so the one consequence a reversal
    could not undo is gone; the gap that remains — nothing edits or deletes a recorded move — is
    restated as what it is, with the stakeholder's own sentence about it. This is propagation of
    the answer into a section the answer changed, not a widening of scope.
  - **The five criteria round 1 listed for round 2 were deliberately not written.** The success
    output, the streams and exit codes, zero and negative, a move to and from the same envelope,
    and the wrong number of words are every one of them `refine`'s own `[assumed]` decision or a
    delivered convention, and none was asked in `Q-001`. Putting an assumption into a criterion is
    refinement's judgement taken in the open rather than a propagation — the same line this skill
    drew on `WI-0003` in the execution immediately before this one.
  - **No item filed.** The answer implies no work this item does not already cover: `--on` on a
    move is this item's own command surface, and the correction gap it mentions was already
    recorded in `## Out of scope` and belongs to nobody's criteria.
  - **No document under `docs/` was changed**, and no `## Engagement state` section was written or
    amended. Nothing in this answer is a fact about the engagement.
- **Questions raised:** none — every cross-answer verdict came out `compatible`, and the reply left
  nothing the record could not settle.
- **Commands:**
  - `.claude/agile-skills/scripts/lint-answers --item WI-0004` → exit 0 (1 consumed human answer,
    0 delegations, 0 errors, 0 warnings)
  - `.claude/agile-skills/scripts/lint-documents --rule propagated-claims-carry-their-obligation --item WI-0004 --uncommitted` → run by the transition, exit 0
  - `.claude/agile-skills/scripts/lint-documents --rule engagement-state-is-left-to-the-ending --uncommitted` → run by the transition, exit 0
  - `.claude/agile-skills/scripts/validate-workspace` → run by the transition with the move resolving, exit 0
- **Gates:**
  - `answer-is-propagated` → **pass** (`Q-001`'s `## Consequences` names seven changes across two files, and every one was re-opened after writing: `item.md` AC1 carries `--on <date>` and the worked line `envel move groceries fun 20 --on 2026-08-28`; AC6, AC7 and AC8 exist and state the default, the accepted form and the future-date refusal; `## Out of scope`'s correcting-a-move entry carries the amended sentences; `## Notes` carries what the answer settled and what is left for round 2; `refinement-qa.md` carries `## Answers — round 1` with the reply verbatim. No Consequences section names zero files.)
  - `answered-from-the-record` → **pass** (the answer was not produced by this skill — it is the stakeholder's own reply to an escalation, quoted verbatim in `## Answer` and again in `refinement-qa.md` `## Answers — round 1`; the three supporting citations written into AC6, AC7 and AC8 all resolve, checked by reading `WI-0002` AC9, AC11 and AC12 directly)
  - `escalation-is-justified` → **pass** (no question was re-addressed to the human by this execution; the one question it handled was already an escalation filed by `refine` round 1, and it is now returned)
  - `propagated-claims-carry-their-obligation` → **pass** (`lint-documents` exit 0; no sentence was written into `docs/` at all, so there is no cited fact and no quantified claim to discharge)
  - `engagement-state-is-left-to-the-ending` → **pass** (`lint-documents` exit 0; no `## Engagement state` section was written or amended, and this answer falsifies no sentence in one — it is about when a move happened, not about the engagement)
  - `cross-answer-consistency` → **pass** (`lint-answers --item WI-0004` exit 0; five verdicts, all `compatible`, no conflict, so no question was filed under ADR-0008 §3 — checked against `WI-0002/Q-001`, `WI-0003/Q-003`, `WI-0003/Q-001`, `EP-001/Q-002` and `EP-001/Q-005`; no claim in `docs/` sourced to a human answer was rewritten, none being touched)
  - `workspace-valid` → **pass** (`validate-workspace` run by this transition with the move resolving, exit 0)
  - `item-resumed-correctly` → **pass** (the suspending row of 2026-09-11T05:13:08Z records `resume-to: draft`; this execution moves the item to `draft` and to nothing else, the item's only blocking question now being `answered`)
  - `a-deferral-is-not-an-answer` → **pass** (the reply did not defer — it chooses option A by letter, gives a reason, and names the project fact that settled it; nothing in it postpones anything)
- **Cross-answer check:**
  - `Q-001` — checked against `WI-0002/Q-001` (compatible, and the answer this reply follows: the same rule and the same reason, *"I move the money because of a shop I'm typing in late"*), `WI-0003/Q-003` (compatible, and the pair round 1 flagged: income is still dated when it is typed, `envel add` is untouched, and the stakeholder did not frame this as changing it), `WI-0003/Q-001` (compatible: a move is still kept out of *spent* and shown as one net figure; this settles only which month it counts in), `EP-001/Q-002` (compatible: the overspend rule and AC3 are untouched by a date on the line), `EP-001/Q-005` (compatible, and the reply leans on it: correction was scoped to spends there, and the stakeholder cites that scoping as their reason here rather than revising it).
  - No verdict was `conflicts`, so no question was filed and no document was edited in place of asking.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-001.md` — `status: answered`, `answered-by: human`,
    `answered-at` stamped, `## Cross-answer check` written with five verdicts, `## Consequences`
    naming seven changes across two files
  - `tracker/items/WI-0004/item.md` — AC1 amended in place; AC6, AC7 and AC8 appended;
    `## Out of scope`'s correcting-a-move entry amended; `## Notes` gained what the answer settled,
    that neither prior answer was overturned, the stakeholder's project-fact reason, and round 2's
    remaining job
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — `## Answers — round 1`,
    `## Cross-answer check — round 1, on the reply` and `## What round 1's answer left for round 2`
    added; the header paragraph and `## What round 1 has not settled` updated
  - no ADR created, no document under `docs/` touched, no new item filed
  - commit: `tracker: the answered questions and every artifact you propagated into (refs WI-0004)`
- **Status:** `awaiting-answer` → `draft`
- **Result:** The one thing `WI-0004` could not derive is settled: a move carries `--on` and is
  held against the date given, exactly as a spend is. AC1 says so and AC6–AC8 carry the three date
  rules by citation to the delivered `envel spend`. Neither of the stakeholder's two earlier,
  opposite answers was overturned, and the item returns to `draft` for `refine` round 2, whose job
  is now the five assumed criteria and the Definition of Ready.

## 2026-09-11T05:33:18Z — refine v0.6.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft`, dispatched by `next` — round 2, resumed after `answer-questions` returned the item from `awaiting-answer` on consuming `Q-001`'s reply
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`
  - `tracker/items/WI-0004/history.md` — the item reached `draft` by resuming from `awaiting-answer`, not by a send-back from `verifying` or `in-review`, so this is round 2 of a first refinement rather than a repair of a specific defect
  - `tracker/items/WI-0004/journal.md`
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — round 1's record, including the bounded job it left round 2
  - `tracker/items/WI-0004/questions/Q-001.md` — answered and propagated; nothing open on this item
  - `tracker/items/WI-0001/item.md` and `tracker/items/WI-0002/item.md` — the delivered criteria this item cites rather than re-decides
  - `tracker/items/WI-0003/item.md` — the summary that is the only place a move is ever displayed
  - `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md`, `ADR-0003-store-location.md`, `ADR-0006-a-spend-carries-the-date-it-happened.md`
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/doc-header.md` §4a
- **Decisions:**
  - **Wrote the five criteria round 1 deferred, and asked nobody about any of them.** AC9 (the success line names both envelopes and both new amounts), AC10 (zero and negative refused), AC11 (a move to and from the same envelope refused), AC12 (streams and exit codes), AC13 (the wrong number of words). Rationale, per skill step 3 applied to each: AC10 is the third instance of a rule the stakeholder stated once for income at `WI-0001/Q-003` and that `WI-0002` AC6 has already shipped under, so re-asking would tell them their answer was not heard; AC12 and AC13 are not decisions at all but the project's delivered conventions, written in by citation; AC9 and AC11 are `refine`'s own `[assumed]` decisions from round 1, which `Q-001` had already shown them in as many words and which their reply did not contest. Inventing a second round trip over decisions they had already seen is the failure step 3 names from the other side.
  - **Amended AC1 and AC6 in place to name how a move's stored date is observed.** Rationale: both said what the date *means* without saying where anybody would look, and nothing this item delivers prints a move's date back — `WI-0003`'s summary is the first thing that would, and it is neither delivered nor a dependency of this item. So neither criterion was decidable by a person with a terminal, which is R4. The repair is the route the delivered item already uses for exactly this situation: a store of its own under `ENVEL_FILE` [src: ADR-0003], read directly [src: WI-0002 AC8 "Observed in a store of its own"]. This is a decidability repair and not a change of meaning — what the stakeholder chose at `Q-001` is untouched — and it is recorded as `refine`'s own judgement rather than as propagation, because propagating an answer and making a criterion decidable are different jobs.
  - **Amended in place rather than inserting, so no criterion changed its number**, and re-ran the renumbering check after the append [src: run: grep -rn 'WI-0004 AC' tracker docs → exit 0, 5 lines, all of them the command quoted inside backticks]. Rationale: a citation naming a number goes on resolving against whatever moves into that position, silently (F-094).
  - **Disposed of every combination R10 reaches, without deciding the one that is `plan`'s.** `--on` with each refusal is left **deliberately unconstrained** in `## Notes` and routed to `plan`, with who left it so — the same question `WI-0002` routed there, and every criterion stays satisfiable under any ordering `plan` picks, because each requires only that nothing moves. `--on` malformed at the parser is left the same way, with AC12 still binding its stream and exit code. How an amount may be written is delivered and cited rather than restated, as `WI-0002` also chose. Rationale: R10 forces a combination to be *visible*, not decided, and deciding `plan`'s question here would be the scheduler-style leak in a different skill.
  - **Recorded the back-dating-versus-balance reading outright.** AC3 refuses a move larger than what is *currently* in the source envelope, and a move is now datable, so the two could have been read as contradicting. They do not: the delivered spend checks the present balance for a back-dated spend too [src: WI-0002 AC5 "Recording a spend larger than the amount currently in the envelope is refused"], and the reply to `Q-001` asked for a move *"datable, same as a spend"*. Reading it any other way would extend their answer past what it says. Stated in `## Notes` rather than left implicit in AC3's one word.
  - **Marked round 1's "this item is not Ready" note as superseded rather than deleting it.** Rationale: it was true when written and the record should show that it stopped being true, and why.
  - **Recorded no override.** Every Definition of Ready criterion passes on its own terms, so naming one as unmet would be a false entry.
- **Questions raised:** none — round 2 put nothing to the stakeholder, and `artifacts/refinement-qa.md` `## Round 2` states the test applied to each of the five criteria and why each failed to be theirs. The only question ever filed on this item, `Q-001`, is `answered`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 7 items, 8 documents, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/lint-answers --item WI-0004` → exit 0, 1 consumed human answer, 0 delegations spent, 0 errors, 0 warnings
  - `grep -rn 'WI-0004 AC' tracker docs` → exit 0, 5 lines, every one the command itself quoted inside backticks
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace` → exit 0, 0 errors, 0 warnings, run after every edit including the last)
  - `definition-of-ready` → **pass** (walked criterion by criterion, with the table in `artifacts/refinement-qa.md` `## Definition of Ready — round 2's walk` carrying the evidence for each. R1 pass (frontmatter complete, validator green); R2 pass (`## Story` names the role, the capability and the outcome); R3 pass (thirteen labelled checkbox criteria); **R4 pass — was failing at the start of round 1** (AC1 and AC6 gained the store observation; no criterion carries an unmeasurable adjective, and message *wording* is deliberately unconstrained with each criterion saying what a message must contain); R5 pass (four exclusions, the first being the gap a reader would assume `WI-0005` covered); **R6 pass — failed during round 1 by round 1's own act** (`Q-001` answered, nothing open); **R7 pass — was failing at the start of round 1** (`depends-on: WI-0001`, which is `done`); **R8 pass — was failing at the start of round 1** (`refinement-qa.md` exists and declares `status: recorded` over a conversation that happened); R9 pass (one subcommand, one coherent change); **R10 pass — was failing at the start of round 1** (`## Notes` `### Combinations` disposes of every one — `--on` against each refusal and against the parser left deliberately unconstrained and routed to `plan` with who left it so, `--on` with the wrong word count at AC13, the amount form delivered and cited, the back-dating-versus-balance reading stated); R11 pass (nothing is counted; AC12 names the criteria it covers by ID and says the assessment is a read of their text with the suite as evidence rather than as definition); R12 pass (five `[assumed]` decisions, every one saying `under no delegation` and naming where a disagreement lands — there is no standing delegation in this engagement, and `lint-answers` reports 0 delegations spent). **No override.**)
  - `criteria-are-decidable` → **pass** (a command or artifact and the verdict that follows is written out for all thirteen criteria in `artifacts/refinement-qa.md` `## How each criterion is decided — round 2`. AC12 is the one whose subject is other criteria; it names them by ID, asks for a read of their text with the suite as evidence, and says what to do when nothing executable exercises a named criterion — state the non-intersection, then add a covering case or waive it by name.)
  - `cross-answer-consistency` → **pass** ((`lint-answers --item WI-0004` → exit 0). Round 2 consumed no human answer, so `Checked against: none`, and the Q&A says why that is a result rather than an omission. The one thing read across anyway was AC3's balance check against the back-dating `Q-001` introduced; they are compatible on the delivered spend's own precedent, and no answer of theirs was edited to make it so.)
  - `qa-recorded-verbatim` → **pass** (`artifacts/refinement-qa.md` carries round 1's question and the stakeholder's reply verbatim, and round 2's section states plainly that round 2 asked nothing. Every `[assumed]` answer carries `under no delegation` in terms and names where a disagreement lands; none is taken under a standing delegation, so no `**Under delegation:**` line is owed.)
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` (updated — AC1 and AC6 amended in place, AC9–AC13 appended, `## Notes` gained the round 2 record and the combinations section)
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` (updated — `## Round 2`, `## Cross-answer check — round 2`, `## Definition of Ready — round 2's walk`, `## How each criterion is decided — round 2`)
  - `tracker/board.md` (regenerated)
- **Status:** `draft` → `ready`
- **Result:** `WI-0004` meets the Definition of Ready. Round 2 wrote the five criteria round 1 deferred, repaired the two criteria that stated a date's meaning without stating where it is observed, and disposed of every combination R10 reaches — three of them by routing to `plan` in the open rather than deciding them here. Nothing was put to the stakeholder, and the Q&A records the test that produced that answer for each criterion.

## 2026-09-11T05:41:18Z — plan v0.6.3 — architect

- **Item:** WI-0004
- **Trigger:** status `ready`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the thirteen criteria this design is contracted to
  - `tracker/items/WI-0004/history.md` — a first plan, not a re-plan: the item reached `ready` from `draft` by `refine`, never from a rejection
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — the five `[assumed]` decisions and the three questions `refine` routed here rather than to the stakeholder
  - `tracker/items/WI-0004/questions/Q-001.md` — the stakeholder's answer that a move is datable
  - `tracker/items/WI-0003/item.md` — AC2 and AC3, the net moved figure this item has to make computable
  - `tracker/items/WI-0001/item.md`, `tracker/items/WI-0002/item.md` — the delivered criteria this change must not falsify, AC14 and AC15 of `WI-0001` in particular
  - `docs/architecture/overview.md` (v4, read before updating it to v5)
  - `docs/product/vision.md` (v2)
  - Every ADR, by number: `ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006`
  - `envel/envelopes.py`, `envel/cli.py`, `envel/store.py`, `envel/money.py`, `envel/dates.py`
  - `tests/test_cli.py`, `tests/test_envelopes.py` — the two classes this change extends and the helpers they already have
  - `tracker/project.yaml`
- **Decisions:**
  - **A move is two entries of kind `move`, one per envelope, opposite signs, sharing one `on` and one `at`.** `ADR-0007`, written this execution. Branch of the preference order: the documents *forced* it rather than answered it — `ADR-0002` makes a balance the plain sum of `cents` over the entries naming an envelope, so a single entry naming two envelopes would put a special case into the one function every command in the tool depends on. The alternatives (one entry with `from`/`to`; two entries of distinct kinds `move-out`/`move-in`) are in the ADR with their costs. The consequence worth naming is that AC2 — source down by exactly the amount, destination up by exactly it, nothing else changed — becomes a property of the storage rather than something the code arranges.
  - **A move's date lives in `on`, `YYYY-MM-DD`, exactly as a spend's does.** Answered from the documents: `ADR-0006` already defines `on` as the day an event is held against, and the stakeholder asked for a move *"datable, same as a spend"*. No new field and no new meaning for `at`.
  - **The two entries of a move are not linked to each other.** Recorded as a reversible assumption with its honest cost: adding a pairing field later is one field in one function and needs no migration to read the file, but moves recorded before the change could not be paired. Nothing in this epic reads the pair — `WI-0003` wants a net figure, `WI-0005` is scoped to spends, `WI-0006` to the spends against an envelope — so inventing an identifier now would be designing past the item.
  - **The order of the six refusals**: source missing, destination missing, same envelope, amount not positive, date in the future, source holds too little. This is one of the three questions `refine` routed here. Rationale: the existence checks lead so that a message naming an envelope is always available, which is what AC4 promises and what `WI-0002` decided for the same reason; the same-envelope check joins them because it is the third question about the *names*; the funds check is last because its message has to quote a balance, which is only meaningful once the envelope exists. Recorded under `## Assumptions` as reversible — one function and one test.
  - **Two refusals are reached before the operation at all**, because a malformed amount and a malformed date are raised where they are parsed in `envel/cli.py`. Named in the plan rather than left to be discovered: `envel move nosuch fun 1 --on 28/8` reports the date, not the envelope, and `envel spend` behaves the same way today.
  - **No new module.** Answered from the documents: the overview's module table and its one-way dependency direction already say that an operation goes in `envelopes` and that only `cli` touches a stream. `money` and `dates` already exist for exactly the parsing this needs.
  - **`dest="source"` / `dest="destination"` with `metavar="from"` / `metavar="to"`.** Decided; no alternative worth an ADR. `from` is a Python keyword, so the obvious `dest="from"` cannot be read back off the namespace, and the metavars keep the usage line reading `envel move from to amount`.
  - **`move` is added to the top-level subcommand `metavar`.** Answered from the documents, and it is the one thing in this change that could break *another* item: `WI-0001` AC14 requires the usage message to list the subcommands the tool has. Recorded as a risk as well as a step, because `WI-0002` hit it and answered it with a test.
  - **The balance check reads the present balance, not the balance on the date given.** Answered from the documents — the delivered spend does the same for a back-dated spend, and `refine` had already recorded the reading. Not a free choice, so it is an assumption only in the sense that reversing it is one comparison.
  - **The third question `refine` routed here — what a move does with a stored entry naming an envelope that is no longer present — is not decided, because it cannot arise.** Nothing in this tool deletes an envelope, so no entry can name an absent one. Recorded here rather than in the plan because the honest answer is that the question has no subject yet; the item that introduces deletion is the one that has to answer it.
  - **`docs/architecture/overview.md` updated to v5** rather than left to `implement`: this change alters the shape of the data, which is exactly the condition for touching it.
  - **`tracker/project.yaml` untouched.** `commands.test` and `commands.lint` are already real commands and were run this execution.
- **Cross-answer check:** `none` — this execution recorded no new human answer and relied on no answer that was not already consumed and propagated. It did read two of theirs across each other, and the plan says so: `WI-0004/Q-001` (a move is datable like a spend) against `WI-0003/Q-001` (a move is kept out of *spent* and shown as a net figure). They are compatible and jointly constrain the storage rather than conflicting — the first says a move carries `on`, the second says `WI-0003` must be able to filter and sum move entries by envelope and month, and `ADR-0007` satisfies both. No answer of theirs was edited, and no ADR written here settles a disagreement between two things they said.
- **Questions raised:** none. Every decision was answerable from the documents or reversibly assumable; nothing here is irreversible before any code exists, and nothing turned on intent the record does not hold.
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, 90 tests
  - `python3 -m compileall -q envel tests` → exit 0
  - `grep -rn '"move"' envel` → exit 1, no output (the reversibility claim in `ADR-0007`)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before this entry existed, with exactly two `doc.changelog.no-execution` errors naming the two rows this execution wrote; exit 0, 0 errors, 0 warnings when re-run after the entry existed. See the `workspace-valid` gate line.
  - `python3 .claude/agile-skills/scripts/lint-claims --uncommitted` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/lint-answers --uncommitted` → exit 0, 21 consumed answers, 0 delegations spent
  - `python3 .claude/agile-skills/scripts/lint-documents --rule documents-at-risk-are-enumerated --item WI-0004` → exit 0, 19 invalidation rows, 0 deliverable documents, 7 binding ADRs
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass when run directly; the transition was taken with `--force`.** Read this one in full, because the record must not overstate it.
    - Run on its own against the state this entry describes, `validate-workspace` reports **0 errors, 0 warnings**. The state is sound.
    - It could not be made to report that *from inside the transition*, and the deadlock is F-084's, reached by `plan` for the third time in this engagement — `WI-0001`, `WI-0002`, and now this item. Writing `ADR-0007` and bumping `docs/architecture/overview.md` puts two `doc.changelog` rows in the workspace saying *plan changed this for `WI-0004`*. `doc.changelog.no-execution` checks `WI-0004`'s journal for an execution of `plan`, and the only entry that can satisfy it is the one `transition` appends **after** its gates have run. `--resolving 'WI-0004:ready->planned+journal'` does not cover it: `resolved_by_move` downgrades `journal.execution.missing` for exactly this reason (its own comment cites F-025) and does not include `doc.changelog.no-execution`, which is the same shape one rule along.
    - The two rows are otherwise correct and will be inside the window the moment the entry exists: `WI-0004`'s previous journal entry closes at `2026-09-11T05:33:18Z` and the rows are stamped `05:35:47Z` and `05:38:33Z`, both after it and both before this entry.
    - So the move was made with `--force`, which skips the gate run and records `[gates forced]` in the history reason for ever. **Every gate below was run by hand before that, and each passed**; the commands and their exit codes are under `**Commands:**` and can be re-run. `validate-workspace` was re-run immediately after the transition and reports 0 errors, which is the state a reader can check now.
    - This is a toolkit finding rather than a fact about this change: three of three `plan` executions in this engagement have been forced for it, and the fix is one code in `resolved_by_move`. `WI-0001`'s plan entry predicted `plan` could not avoid it *"for the first item it plans"*; the prediction was too narrow — it recurs on every item whose plan touches a document, which is most of them.
  - `every-criterion-is-addressed` → **pass** — `## Acceptance criteria mapping` has one row per criterion, AC1 through AC13, each naming the step that satisfies it and a specific observation rather than "tests": the store file read after a dated move, the listing compared before and after, the named refusal messages, the two subprocess invocations, and the four wrong-argument lines. AC12's row names the case each criterion it covers contributes, which is what that criterion asks for.
  - `project-commands-resolved` → **pass** — `commands.test` is `python3 -m unittest discover -s tests -t .` and `commands.lint` is `python3 -m compileall -q envel tests`; both were run this execution and both exited 0 against real work (90 tests). Neither needed filling in.
  - `decisions-recorded` → **pass** — `## Decisions and ADRs` lists seven choices, each pointing at `ADR-0007` or at a `## Assumptions` entry stating what reversal costs. The three reversible assumptions each name the file and the artefact that would change, and each says plainly that it is taken under **no** standing delegation, there being none in this engagement.
  - `plan-is-executable-without-you` → **pass** (advisory) — the seven steps each name the file, what is added, and what is true afterwards. The two places a developer would otherwise have to decide are decided in the open: the refusal order, and the two argparse `dest`/`metavar` names that `from` being a keyword forces. No step asks a downstream skill to do something its contract forbids — the plan says in as many words that ticking a criterion is `verify`'s, and that `implement` may write under `docs/` only to close an invalidation row.
  - `documents-at-risk-are-enumerated` → **pass** (`lint-documents --rule documents-at-risk-are-enumerated --item WI-0004` → exit 0). Nineteen rows, written from opening `docs/product/vision.md`, `docs/architecture/overview.md` and all seven ADRs rather than from recalling them. Dispositions are left open for `implement` except the two `engagement-state` rows, which are `owned-by-ending`. `## Deliverable documents` is `none` — no criterion of this item has a document as its subject — and `## Binding ADRs` names all seven.
  - `cross-answer-consistency` → **pass** (`lint-answers --uncommitted` → exit 0, 0 errors). No new answer was recorded; the two answers read across each other are compatible and the plan says why.
  - `claims-are-sourced` → **pass** (`lint-claims --uncommitted` → exit 0, 0 errors, 0 warnings). Two absolutes were repaired before the gate went green: `ADR-0007`'s *"no new field"*, now stating which ADR each field comes from, and three `[src: WI-0004 AC1]` citations, which a bare number could not carry while the item's criteria may still move — they now quote the criterion's words.
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/plan.md` (new)
  - `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` (new, v1)
  - `docs/architecture/overview.md` (updated, v4 → v5)
  - `tracker/board.md` (regenerated)
- **Status:** `ready` → `planned`
- **Result:** `WI-0004` is designed. One ADR records the only decision with a real alternative — a move is two entries rather than one, because a balance is the plain sum of the entries naming an envelope and a two-envelope entry would special-case that. Seven steps name the files and the observable result; every criterion maps to a specific observation; nineteen documents-at-risk rows are open for `implement` to close. Nothing was asked of the stakeholder, and the one question `refine` routed here that has no subject yet — an entry naming a deleted envelope — is recorded as such rather than answered.

## 2026-09-11T05:42:08Z — implement v0.6.1 — developer

- **Item:** WI-0004
- **Trigger:** status `planned`, dispatched by `next`
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the thirteen criteria
  - `tracker/items/WI-0004/history.md` — the last row is `ready → planned` by `plan`, not a send-back from `verifying` or `in-review`, so this is a first implementation and not a defect fix
  - `tracker/items/WI-0004/artifacts/plan.md` — seven steps, the AC mapping, nineteen invalidation rows, `none` deliverable documents, seven binding ADRs
  - `tracker/items/WI-0004/questions/Q-001.md` — `answered`, and its consequences are already in the criteria; nothing was read out of it to act on
  - `tracker/project.yaml` — `commands.test` and `commands.lint` are both set
  - `envel/cli.py`, `envel/envelopes.py` — the two files the plan changes
- **Decisions:**
  - **Branched from `main` at `4c11b04`**, which is the commit carrying this item's plan and `ADR-0007`, so the branch's own history holds the design it executes.
  - **No reconciliation was needed.** `git branch` showed `wi/WI-0001` and `wi/WI-0002` and no `wi/WI-0004`, so there is no partial work to reconcile with and nothing was redone.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0004 main` → exit 0
- **Gates:**
  - `tests-pass` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `lint-clean` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `workspace-valid` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported PASS here, which decides nothing)
  - `every-criterion-has-a-test` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `commits-reference-the-item` → **pending** (the commit range is empty at this moment; it is inspected at the closing transition; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `no-unplanned-scope` → **pending** (, advisory (there is no diff yet to read); not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported MANUAL here, which decides nothing)
  - `cross-answer-consistency` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `claims-are-sourced` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
  - `document-writes-are-declared` → **pending** (decided at the closing transition of this execution; not decided by this move — `implement` is dispatched again at `in-progress` and this gate is decided there; run-gate reported FAIL here, which decides nothing)
- **Artifacts:**
  - branch `wi/WI-0004`, created from `main` at `4c11b04`
- **Status:** `planned` → `in-progress`
- **Result:** Implementation has started. The branch exists and the item is `in-progress`, so an interruption from here leaves a truthful status; the closing entry is the one that reports the work.

## 2026-09-11T05:53:59Z — implement v0.6.1 — developer

- **Item:** WI-0004
- **Trigger:** status `in-progress`, dispatched by `next`; the closing transition of the execution that opened at `2026-09-11T05:42:08Z`
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the thirteen criteria, unchanged by this execution
  - `tracker/items/WI-0004/artifacts/plan.md` — the seven steps, the AC mapping, the nineteen invalidation rows
  - `tracker/items/WI-0004/questions/Q-001.md` — `answered`; its consequences were read out of `item.md`, which is authoritative, not out of the question
  - `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md`, `ADR-0006`, `ADR-0002`, `ADR-0001`, `ADR-0005`, `ADR-0003`
  - `docs/architecture/overview.md` (v5), `docs/product/vision.md` (v2) — opened, not recalled, to close the invalidation rows against them
  - `envel/envelopes.py`, `envel/cli.py`, `envel/store.py`, `envel/money.py`, `envel/dates.py`
  - `tests/test_envelopes.py`, `tests/test_cli.py` — the helpers and the `Spend` class this change's two new classes are shaped after
- **Decisions:**
  - **Refusal messages follow the delivered wording, minus one clause.** A move's overdraw message says what the source holds and stops there; `record_spend`'s adds *"move money into it first if you want to spend that"*, which would be circular advice on the move command itself. Inside the plan's latitude — `refine` left message wording deliberately unconstrained and the criteria bind only what a message must contain.
  - **Two tests fix the refusal order rather than the plan's one.** The plan asked for the case where the envelope check beats the amount and the date. The half it did not name is the one where both names resolve and the same-envelope check must beat the amount check; without it, half a decision the plan took explicitly would have been unprotected. Recorded as deviation 1.
  - **A fourth malformed date, `2026-13-01`, was added to AC7's test.** The plan named three, all of them wrong in *shape*. `envel/dates.py` refuses a well-shaped impossible day on a different branch, and a test of the shape check alone would never reach it. Recorded as deviation 2.
  - **The shared-moment test replaces `envelopes.now` with a clock that returns a different value on each call.** This was found by mutation, not by reading: with the real clock, computing `at` twice inside one call returns the same string, so the original assertion passed against a deliberately broken implementation. A test that cannot tell the two apart is not evidence of either, so it was rewritten before the work was committed. The fake clock is installed after the document is built, so that `create` and `add_income` do not consume the sequence the move is meant to draw from.
  - **Every criterion's test was mutation-checked, not just run.** Three mutations were applied to `envel/envelopes.py` and reverted: the destination entry's sign (7 failures), the same-envelope refusal removed (4 failures), and `at` computed twice (1 failure, after the test above was strengthened — 0 before). This is the answer to self-check 1, and the third mutation is why the record says the suite was weak and then was not.
  - **One invalidation row was disposed `to-update`; the other seventeen decidable ones are `verified-still-true` and the two `## Engagement state` rows were left alone.** The repair is `ADR-0006`'s `## Consequences`, which enumerated the sums `WI-0003` makes and named two of what are now three. It was repaired as an **erratum** — the clause naming moves, `ADR-0007` cited, a `## Corrections` row and a change-log row, version 2 — following the precedent `implement` set on `ADR-0002` for `WI-0002`. No decision changed and no code changed to satisfy the new text.
  - **Every quantified row was discharged by enumeration and not by opening what the sentence cites.** Six of them: the modules below `cli`, the entry kinds `balance` could special-case, the command-line date call sites, the fields on a move entry, the writes to `entries`, and every import in the package. Each carries its command, the command's output, the members by name and a verdict per member, in `impl-report.md` `## Documents`. The one worth naming is *"nothing below `cli` prints or calls `sys.exit`"*: the grep returns `envel/__main__.py:8`, which is **above** `cli` rather than below it — it imports and calls `main` — so it is not a member of the family, and the row says so rather than quietly dropping the hit.
  - **No row was added to the set.** Every document this change touched was already enumerated by the plan.
  - **Nothing was decided that was not mine to decide**, so no question was filed. The two places the plan was silent — a refusal message's wording and how many cases a test needs — are both explicitly within a developer's latitude here.
- **Cross-answer check:** `none` in the sense that matters — this execution edited no claim in `docs/` that is sourced to a human answer. The one document sentence it did change, `ADR-0006` `## Consequences`, carries no `[src: <ITEM>/Q-nnn]` and is a statement about which field `WI-0003` reads, not a quotation of anybody. Two sentences that **are** theirs were read and deliberately left alone: `docs/product/vision.md` `## What it is for`, which cites `EP-001/Q-005` and `EP-001/Q-002` for moving money being wanted and an overspend being refused, was disposed `verified-still-true` — this change makes it true rather than false, and nothing they have said since overtakes it.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0004 main` → exit 0 (opening entry)
  - `python3 -m unittest discover -s tests -t .` → exit 0, 119 tests, on the branch head after the last change
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → exit 0, all 2 commits on `main..wi/WI-0004` name `WI-0004`
  - `python3 .claude/agile-skills/scripts/lint-answers --changed-since main` → exit 0, 0 errors
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main --plan-documents WI-0004` → exit 0, 0 errors; scope was 7 documents — 1 changed on the branch plus the 7 the plan names
  - `python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item WI-0004 --changed-since main` → exit 0; 1 document written on the branch, 7 named by the plan
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 before this entry existed, with exactly one `doc.changelog.no-execution` on `ADR-0006`'s v2 row; exit 0 once the entry existed. See the `workspace-valid` gate line
  - mutation checks (applied to `envel/envelopes.py` and reverted, `git status` clean afterwards): destination sign flipped → 7 failures; same-envelope refusal deleted → 4 failures; `at` computed twice → 1 failure
  - `grep -rn "print(\|sys.exit\|sys\.std" envel/*.py` excluding `cli.py` → exit 0, 1 line
  - `grep -n '"kind"' envel/*.py` → exit 0, 4 lines, all writes
  - `grep -rn "^import \|^from " envel/*.py` → exit 0, 12 lines, all standard library or intra-package
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` → exit 0, 119 tests, run on the branch head after the last change rather than before it)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` → exit 0)
  - `workspace-valid` → **pass when run directly; the transition was taken with `--force`.** Read this one in full, because the record must not overstate it.
    - Run on its own against the state this entry describes, `validate-workspace` reports **0 errors, 0 warnings**.
    - It could not report that from *inside* the transition, and the deadlock is F-084's — the fourth time this engagement has hit it and the second time this turn. Repairing `ADR-0006` put a change-log row in the workspace saying *implement changed this at `2026-09-11T05:50:35Z` for `WI-0004`*. `doc.changelog.no-execution` asks whether an execution of `implement` on `WI-0004` was running then, and the windows come from the journal: an entry's window is `(previous entry, this entry]` (`scripts/lib/record.py`, `execution_windows`). The opening entry closes at `05:42:08Z`, so the row sits after every window that exists and inside the one this very entry creates. `--resolving 'WI-0004:in-progress->verifying+journal'` does not cover it: `resolved_by_move` downgrades `journal.execution.missing` for precisely this ordering (its comment cites F-025) and does not include `doc.changelog.no-execution`, which is the same problem one rule along.
    - The row is honest and I did not restamp it. `spec/journal-and-history.md` §0 requires a change-log row's `when` to be read from a clock at the moment it is written, and `05:50:35Z` is when it was written. Moving it back to `05:42:08Z` would have made the gate green by recording a time that is not true, which is the failure §0 exists to prevent.
    - So the move was made with `--force`, which skips the gate run and records `[gates forced]` in the history reason for ever. **Every gate below was run by hand before that, and each passed**; the commands and their exit codes are under `**Commands:**` and can be re-run. `validate-workspace` was re-run immediately after the transition and reports 0 errors.
    - **Why `implement` escaped this on `WI-0002` and not here**, because the difference is informative rather than a fact about this change: `WI-0002`'s `ADR-0002` correction is stamped `04:06:14Z`, which is exactly its opening entry's timestamp, so it landed on the inclusive upper bound of a window that already existed. That is luck about a one-second clock, not a technique. Any repair that takes longer than the transition that preceded it deadlocks.
  - `every-criterion-has-a-test` → **pass** — `impl-report.md` `## Acceptance criteria evidence` names a test function for each of AC1 through AC13; none is demonstrated by reading the code. AC12 is the one whose subject is other criteria: `tests.test_cli.Move.test_every_refusal_goes_to_stderr_and_every_success_to_stdout` walks a table keyed by criterion ID — refusals AC3, AC4, AC7, AC8, AC10, AC11, AC13 and successes AC1/AC2/AC9, AC6, AC5 — so **every** criterion AC12 names has an executable case, AC12's non-intersection clause is not reached, and nothing was waived.
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0004 wi/WI-0004` → exit 0, all 2 commits on `main..wi/WI-0004` name the item)
  - `no-unplanned-scope` → **pass**, advisory — the diff against `main` is `envel/envelopes.py` (one function appended), `envel/cli.py` (a subparser, the top-level `metavar`, one dispatch branch), the two test files, and `ADR-0006`'s erratum. Every hunk traces to a plan step or to an invalidation row. The `metavar` hunk is the one that looks unrelated and is not: `WI-0001` AC14 requires the usage message to list the subcommands the tool has, and the plan named it as a step and as a risk.
  - `cross-answer-consistency` → **pass** (`lint-answers --changed-since main` → exit 0, 0 errors, and the `**Cross-answer check:**` bullet above is the read behind it)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main --plan-documents WI-0004` → exit 0, 0 errors). The **scope** the run printed: 7 documents in 7 paths — 1 path differing from `main` under `docs` plus the 7 named by `WI-0004`'s plan, with citations checked across every markdown file in the workspace. A window that could contain nothing would not be a pass, and this one contained the document that was actually repaired.
  - `document-writes-are-declared` → **pass** (`lint-documents --rule document-writes-are-declared --item WI-0004 --changed-since main` → exit 0; 1 document written under `docs/` on this branch, 7 named by the plan, and all nineteen invalidation rows carry a disposition)
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/impl-report.md` (new)
  - `tracker/items/WI-0004/artifacts/plan.md` (updated — the `disposition` column only)
  - `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` (updated, v1 → v2, with a `## Corrections` erratum row)
  - `envel/envelopes.py`, `envel/cli.py`, `tests/test_envelopes.py`, `tests/test_cli.py`
  - branch `wi/WI-0004`, commits `f17287e` and `96cdd5f` on `main..wi/WI-0004`
- **Status:** `in-progress` → `verifying`
- **Result:** `envel move` is built and handed to verification. Thirteen criteria, twenty-seven new tests, 119 in the suite and green; the three mutations tried against it all fail, including one that passed until the shared-moment test was rewritten. All nineteen invalidation rows are disposed — one erratum on `ADR-0006`, seventeen verified still true with the enumeration each quantified claim owes, two left to the ending. No criterion was ticked and no question was filed.

## 2026-09-11T06:05:57Z — verify v0.5.1 — qa-engineer

- **Item:** WI-0004
- **Trigger:** `verifying` — `next` dispatched `verify` as the status owner; the item was the
  highest-ranked runnable candidate (priority `medium`, created `2026-09-11T02:12:40Z`), ahead of
  `WI-0005` on `created` and `WI-0006` on priority, with `WI-0003` rejected for `depends-on WI-0004`.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the thirteen acceptance criteria, read **before** the
    implementation report, so that what would settle each one was derived from the criterion
  - `tracker/items/WI-0004/history.md`
  - `tracker/items/WI-0004/artifacts/plan.md` — the binding ADR list (seven) and the invalidation
    set (nineteen entries), and the refusal order and interface decisions the diff was read against
  - `tracker/items/WI-0004/artifacts/impl-report.md` — read after the criteria, and checked rather
    than cited; no verdict in `verify-report.md` rests on it
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — for AC12's and AC13's wording
  - `tracker/project.yaml` — the test and lint commands
  - all seven ADRs under `docs/architecture/adr/`, each `## Decision` in full
  - `docs/architecture/overview.md` and `docs/product/vision.md` — the sentences the invalidation
    set names, reopened against the branch head
  - the code at branch `wi/WI-0004`, commit `fdff4fba588e2ebafc128303f04367ec0cc58ee6`
- **Decisions:**
  - **Every criterion `pass`; none `ambiguous`, none `substituted`.** No criterion named an
    observation this environment cannot make: AC1 and AC6 name the store file under `ENVEL_FILE`,
    which is readable here, so `- [~]` was not reached for. All thirteen are `- [x]` and each is
    backed by a command run by this execution.
  - **No send-back and no bug item.** Nothing failed on this item's own criteria, so the
    send-back question did not arise; and the two places where adding a subcommand could have
    falsified another item's delivered criterion were checked deliberately — `WI-0001` AC14 (the
    tool's usage lists `{new,add,list,spend,move}`) and the `WI-0002` spend path (an overspend is
    still refused, `--on 28/8` still rejected) — and neither is broken, so there was no defect to
    classify.
  - **AC12 was settled as a read of the eleven criteria it names, not as "the suite is green".**
    Each named criterion's sentence was read against the new behaviour and given its own verdict.
    The one place the sentences could have collided is AC13, which exits **2** where the other
    refusals exit 1; AC12's own wording is "exits non-zero", so both hold, and that was resolved
    by quoting both rather than by observing that nothing failed. **Non-intersection: none** —
    `tests/test_cli.py:685` asserts `returncode`, `stderr` and `stdout` on the same invocation for
    every criterion AC12 names, so there was no criterion to waive by name. The eleven cases were
    also re-run by hand here with the three captured separately.
  - **Three mutations looked insensitive and the harness was wrong, not the tests.**
    `record_spend` carries the same three guard lines as `move` — `if cents <= 0:`,
    `if on > dates.today():`, `if cents > remaining:` — so a replace-first mutation patched the
    spend's copy and left the move's behaviour intact, and the move test passed because nothing
    had been removed. Caught by running the mutant by hand rather than by trusting the verdict;
    redone against `move`'s own line numbers, where all three tests fail. Recorded in
    `verify-report.md` rather than quietly corrected, because the first result has the shape of a
    real finding and was not one.
  - **Nothing under `docs/` was written.** The one `to-update` entry was checked for the update it
    claims — `ADR-0006` at `version: 2` with a change-log row and a `## Corrections` erratum — and
    the two `owned-by-ending` entries were left exactly as they are; both stale
    `## Engagement state` sections were confirmed untouched by any `WI-0004` commit.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 119 tests … OK`
  - `python3 -m compileall -q envel tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item WI-0004`
    → exit 0, 7 binding ADRs against 7 conformance rows
  - `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0004`
    → exit 0, 19 entries against 19 rows
  - `git rev-parse HEAD` → `fdff4fba588e2ebafc128303f04367ec0cc58ee6`; `git status --short` → clean
  - `git diff main...HEAD -- envel/ docs/` → the whole source and docs diff, read against the plan
  - AC1: `envel new groceries`, `envel new fun`, `envel add groceries 100`,
    `envel move groceries fun 20 --on 2026-08-28` → exit 0; `cat $ENVEL_FILE` → two `move` entries
    carrying `on: "2026-08-28"`
  - AC2: three envelopes at `100`/`5`/`42.50`, `envel list` before and after
    `envel move groceries fun 20`, `diff` → exactly two changed lines
  - AC3: `envel move groceries fun 30.01` against `30.00` → exit 1, stderr names `groceries` and
    `30.00`; `envel move groceries fun 30` → exit 0 (the boundary)
  - AC4: `envel move nosuch fun 5`, `envel move groceries nosuchdest 5`,
    `envel move nosuch alsonosuch 5` → exit 1 each, the named envelope in the message
  - AC5: `envel move …` in one process, `envel list` in a second → the amounts as the move left them
  - AC6: `envel move a b 1` and `envel move a b 2 --on 2020-01-01`, store read → `2026-09-11` and
    `2020-01-01`; `date -u +%F` → `2026-09-11`
  - AC7: `--on` given `28/8`, `08-28`, `yesterday`, `2026-8-28`, `20260828`, `2026-02-30` → exit 1
    each; `--on 2026-08-28` → exit 0
  - AC8: `--on 2026-09-12` and `--on 2027-09-11` → exit 1 each; `--on 2026-09-11` → exit 0
  - AC9: `envel move groceries fun 20` with streams captured separately → stdout carries all four
    values, stderr empty, exit 0; `envel move fun groceries 20` restores both balances
  - AC10: `0`, `0.00`, `-5`, `-- -5` → exit 1 each, listing string-identical before and after
  - AC11: `groceries→groceries`, `groceries→Groceries`, `GROCERIES→groceries` → exit 1 each
  - AC13: `envel move`, `envel move groceries`, `envel move groceries fun`,
    `envel move groceries fun 20 extra` → exit 2 each, `usage: envel move …` on stderr
  - AC12: one invocation per criterion it names, stdout/stderr/exit captured separately → tabulated
  - ADR-0004: `python3 -m envel move a b 3` → exit 0; `python3 bin/envel move b a 1` → exit 0
  - invalidation audit: `grep -n "print(\|sys.exit\|sys\.std" envel/envelopes.py envel/store.py envel/money.py envel/dates.py`
    → exit 1, no hits; `grep -rn "parse_amount\|format_amount\|float(\|/ 100\|\* 100" envel/ --include=*.py`
    → only `money.py` converts; a store carrying income, spend and move at once, read with a
    python one-liner → append-only prefix identical with two appended, `move`'s field set a subset
    of the other kinds', `at` the recording moment on all three kinds, balances by plain sum
    matching `envel list`; an AST walk over `envel/` and `bin/envel` → no network-capable import
  - thirteen mutation runs, one per criterion, each `python3 -m unittest <the named test>` with the
    source restored afterwards and compared byte-for-byte → all thirteen fail under mutation
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, 119 tests, run by this execution on `fdff4fb`, not read from the implementation report)
  - `lint-clean` → **pass** (`python3 -m compileall -q envel tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, 0 errors, 0 warnings, run immediately before this transition)
  - `every-criterion-independently-checked` → **pass** (`verify-report.md` `## Criteria`: thirteen rows, each naming the command this execution ran and quoting its actual output; the implementation report is cited as evidence nowhere)
  - `negative-cases-exercised` → **pass** (`## Negative and boundary cases exercised`: every error, empty-input and boundary case triggered — AC3 at one cent over and at exactly the balance, AC8 at tomorrow and at today, six malformed date forms, a negative amount both bare and behind `--`, all four wrong argument counts, an empty store on every run)
  - `a-criterion-about-criteria-is-read` → **pass** (`## A criterion about criteria`: AC12's eleven named criteria by ID, one verdict each read from their text, the AC13/AC12 exit-code question resolved by quoting both sentences, and non-intersection checked and found absent — so nothing to waive)
  - `adr-conformance-is-decided` → **pass** (`lint-documents --rule adr-conformance-is-decided --item WI-0004` exit 0; `## ADR conformance` carries seven rows, each `conforms` with the `## Decision` clause quoted and a file and line in this change; no ADR outside the plan's list was found engaged, and there are only seven ADRs in the project)
  - `invalidation-set-is-disposed` → **pass** (`lint-documents --rule invalidation-set-is-disposed --item WI-0004` exit 0, 19 entries against 19 rows; seventeen `verified-still-true` reopened and read against the branch head with the enumeration and the falsifier stated for each quantified claim, one `to-update` confirmed updated with a version bump and a change-log row, two `owned-by-ending` left untouched)
  - `tests-would-fail-without-the-change` → **pass** (advisory; `## Test sensitivity check`: thirteen mutations, one per criterion, each making the named test fail, with the two source files restored byte-identical afterwards)
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/verify-report.md` — created
  - `tracker/items/WI-0004/item.md` — AC1–AC13 ticked `- [x]`, thirteen of thirteen, none `- [~]`
  - no bug items filed; no file under `docs/` written
  - commit: `tracker: the verification report and the ticked criteria (refs WI-0004)`
- **Status:** `verifying` → `in-review`
- **Result:** All thirteen acceptance criteria pass against `fdff4fb`, each on evidence this
  execution gathered; seven binding ADRs conform, nineteen invalidation entries are properly
  disposed and the seventeen claiming a document is still true were reopened and found true. No
  defect was found on this item or on any other, so `WI-0004` goes to `in-review` rather than back.

## 2026-09-11T06:15:17Z — review-close v0.14.1 — reviewer

- **Item:** WI-0004
- **Trigger:** status `in-review`, dispatched by `next` as the status owner; highest-ranked
  runnable candidate (priority `medium`, created `2026-09-11T02:12:40Z`), ahead of `WI-0005` on
  `created` and `WI-0006` on priority.
- **Inputs read:**
  - the diff `main...wi/WI-0004`, hunk by hunk — `git diff main...HEAD -- envel/ docs/` and
    `-- tests/`; five files, every hunk mapped to a plan step or an invalidation row
  - `tracker/items/WI-0004/item.md` — the thirteen criteria and their tick state
  - `tracker/items/WI-0004/artifacts/plan.md` — the seven steps, the AC mapping, the nineteen
    invalidation rows, the seven binding ADRs, the assumptions and their reversal costs
  - `tracker/items/WI-0004/artifacts/impl-report.md` — the two declared deviations and
    `## What I did not do`
  - `tracker/items/WI-0004/artifacts/verify-report.md` — the evidence behind each tick and
    `## Not verified, and why`
  - `tracker/items/WI-0004/journal.md` in full — eight entries, including the two that record a
    forced `workspace-valid` gate
  - `tracker/items/WI-0004/history.md` — eight rows, chaining without a gap
  - `tracker/items/WI-0004/questions/Q-001.md` — `answered`, its `## Consequences` checked against
    `item.md`
  - all seven ADRs under `docs/architecture/adr/`, `ADR-0003` and `ADR-0004` in full for D7's open
    question; `docs/architecture/overview.md` and `docs/product/vision.md`
  - `tracker/project.yaml`; `tracker/board.md`
- **Decisions:**
  - **Accept, `outcome: delivered`.** No criterion failed, no defect belongs elsewhere, and nothing
    in the diff is unrequested. The one hunk that looks unrelated — `metavar="{new,add,list,spend,move}"`
    in `envel/cli.py` — is required by a delivered criterion of another item (`WI-0001` AC14) and
    was named by the plan as interface decision 3 and as its first risk; there is a test for it.
  - **The two `[gates forced]` transitions were examined rather than waved through.** The forcing
    is `workspace-valid` alone, for the F-084 ordering deadlock, on `plan` and on `implement`. Both
    journal entries record every other gate run by hand with its command and exit code; I re-ran
    the two that bear on the code (`unittest` → exit 0, 119 tests; `compileall` → exit 0) and
    `validate-workspace` → 0 errors. No gate was recorded as passed without being run, and none
    that bears on whether the code works was skipped. Not a send-back; recorded as finding 1.
  - **D7's open question answered against an enumerated set, not from memory.** Nine documents
    exist under `docs/`; seven are in the invalidation set; the two that are not — `ADR-0003` and
    `ADR-0004` — were read in full with a falsifier each (a second place in the tool that knows the
    store path; a subcommand reachable from one entry point and not the other). Neither is
    falsified, and both falsifiers are the kind this change could plausibly have produced.
  - **D13 is complete by exhaustion.** The project has exactly seven ADRs and the plan's binding
    list names all seven, so there is no ADR the change could engage that the list does not name.
    Conformance per ADR is `verify`'s verdict and was not re-decided.
  - **Seven gaps accepted, each disposed.** Two are `item-filed:WI-0003` — the item exists at
    `ready` with `depends-on: WI-0004`, so this close is what makes it runnable. Five are
    `no-owner`, and each says why it is a limitation recorded rather than work deferred; the
    timezone one in particular is already a **decision** in `ADR-0006` `## Consequences`
    (*"the person's calendar is the local one"*), not an open question.
  - **Two gap rows were being silently dropped by their own gate, and were reworded.** See finding
    3 — `GAP_NONE_RE` matches a gap cell beginning "Nothing", so two real gaps read as the `none`
    sentinel and the gate passed over a table it had only half-read. Caught by reading the gate's
    own count against the table rather than its exit code.
  - **No bug item filed.** The two cross-item checks a new subcommand warrants — `WI-0001` AC14's
    usage list, and the `WI-0002` spend path — both hold, and the one thing that looked like a
    latent defect (the UTC/local split between `at` and `on`) is recorded in `ADR-0006` as
    deliberate and correct, unchanged by this item.
  - **Merge order followed as specified**: trial-merge in a `--detach`ed worktree at `main`, tests
    on the merge result, discard, confirm the trunk did not move, close, then merge for real. The
    close precedes the merge because `commits-reference-the-item` inspects the range not yet on the
    trunk.
  - **The engagement was not ended, and the verdict is the script's.**
    `scripts/engagement-state EP-001` → `active`, *still in flight: WI-0003, WI-0004, WI-0005,
    WI-0006*. No sign-off is due and no `## Engagement state` section was touched.
- **Cross-answer check:** `none` — this execution consumed no human answer. It wrote no claim
  sourced to one, filed no question and recorded no acceptance, so there was nothing to check a
  prior answer against. The one stakeholder answer this item rests on, `WI-0004/Q-001`, was
  consumed by `answer-questions` at `05:22:31Z` and its consistency with `WI-0002/Q-001` and
  `WI-0003/Q-003` was recorded there; I read that reasoning and it still holds — the reply chose
  the spend's rule for a move and overturned neither. `lint-answers --context work-item
  --changed-since main` → exit 0 over 21 consumed answers and 0 delegations spent.
- **Questions raised:** none — no criterion was ambiguous, the change contradicts no ADR, and
  every gap this review accepted had an owner that is either an existing item on the board or
  `none`, so none of them needed a question to become dispatchable.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0004 wi/WI-0004` → exit 0
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → exit 0, all 4
    commits on `main..wi/WI-0004` name the item
  - `python3 .claude/agile-skills/scripts/lint-claims --context work-item --changed-since main`
    → exit 0
  - `python3 .claude/agile-skills/scripts/lint-answers --context work-item --changed-since main`
    → exit 0, 21 consumed answers, 0 delegations
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0004` → exit 0 (not an epic)
  - `python3 .claude/agile-skills/scripts/lint-documents --rule accepted-gaps-are-dispatchable
    --item WI-0004` → exit 1 twice while the table was wrong, then exit 0, *7 accepted gap(s)*
  - `python3 .claude/agile-skills/scripts/lint-documents --rule engagement-state-is-restated
    --item WI-0004 --context work-item` → exit 0, *NOT APPLICABLE — an item close is not an ending*
  - `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed
    --item WI-0004` → exit 0, 19 entries against 19 rows
  - `python3 .claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided
    --item WI-0004` → exit 0, 7 binding ADRs against 7 conformance rows
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings
  - `python3 .claude/agile-skills/scripts/engagement-state EP-001` → `active`
  - `git rev-parse main` → `4c11b04` before the trial; `git worktree add --detach /tmp/wi0004-trial main`;
    `git -C /tmp/wi0004-trial merge --no-ff wi/WI-0004` → clean, 12 files changed;
    `python3 -m unittest discover -s tests -t .` **in the trial** → exit 0, 119 tests;
    `python3 -m compileall -q envel tests` in the trial → exit 0;
    `git worktree remove --force /tmp/wi0004-trial`; `git rev-parse main` → `4c11b04`, unmoved
  - `python3 -m unittest discover -s tests -t .` → exit 0, 119 tests;
    `python3 -m compileall -q envel tests` → exit 0
  - claims audit, against a scratch store holding income, a spend and a back-dated move:
    `grep -n "print(\|sys.exit" envel/envelopes.py envel/store.py envel/money.py envel/dates.py`
    → exit 1; `envel list` → `groceries  67.50` / `fun  20.00` against a hand-computed sum;
    a python set-difference of `move`'s fields against the other kinds' → empty;
    `grep -rn "socket\|urllib\|http\|requests\|ssl" envel/ bin/envel` → exit 1;
    `grep -rn "int(whole)\|% 100\|// 100\|\* 100" envel/*.py` → exit 0, 2 lines, both `money.py`
  - D7's two unnamed documents:
    `grep -rn "store_path\|ENVEL_FILE\|XDG_DATA_HOME\|\.local/share" envel/ bin/envel` → 4 lines,
    3 in `store.py` and one call site in `cli.py`; `python3 -m envel` and `python3 bin/envel` both
    print `usage: envel [-h] {new,add,list,spend,move} ...`, and `move` succeeds through both
  - `find docs -name "*.md"` → 9 documents; `git diff main...HEAD --stat -- envel/store.py bin/
    envel/__main__.py` → empty
- **Gates:**
  - `definition-of-done` → **pass** (`review.md` `## Definition of Done` walks D1 to D13 with a result and its own evidence for each. D7 is a confirmation against the plan's nineteen-row set plus the question the set cannot answer for itself, answered by reading the two documents it does not name. D13 is complete by exhaustion: seven ADRs exist and the plan names seven.)
  - `engagement-state-is-restated` → **pass** (applicable — an item close.** The sections are the ending's and none was touched. `lint-documents --rule engagement-state-is-restated --item WI-0004 --context work-item` says so in as many words and exits 0. Recorded as not applicable rather than passed (`spec/doc-header.md` §4a).)
  - `accepted-gaps-are-dispatchable` → **pass** (`lint-documents --rule accepted-gaps-are-dispatchable --item WI-0004` → exit 0, *7 accepted gap(s)*. Worth reading with finding 3: the first two runs exited 1 on a malformed table, and a third reported *5* gaps over a seven-row table because two rows began with the word "Nothing". Both were reworded before the close, so all seven are gated rather than five.)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness WI-0004 wi/WI-0004` → exit 0: verified at `fdff4fba`, the branch has since moved to `e9f9e122` but only under `tracker/`, so the verification still covers the code. Run, not judged by eye.)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0004 wi/WI-0004` → exit 0, all 4 commits on `main..wi/WI-0004` name `WI-0004`. Run before the merge, while the range is still non-empty.)
  - `tests-pass-on-the-merge-result` → **pass** (`python3 -m unittest discover -s tests -t .` run **inside** the detached trial worktree after `git merge --no-ff wi/WI-0004`, not on the branch: exit 0, 119 tests. `compileall` in the same worktree → exit 0. `git rev-parse main` returned `4c11b04` both before and after, so the trial moved nothing.)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings, run immediately before this transition and again after the review was rewritten.)
  - `record-is-reconstructible` → **pass** (answered from the tracker, `docs/` and `git log` alone: *what was built and why* — one subcommand moving money between two envelopes, because the stakeholder chose a refused overspend over a negative envelope at `EP-001/Q-002` and asked for moving at `EP-001/Q-005`; *which skill decided what* — `refine` took four decisions under no delegation and routed the refusal order to `plan`, `plan` recorded `ADR-0007` and settled that order, `implement` took two declared deviations, `verify` ticked nothing it had not run; *what questions arose and how they resolved* — one, `WI-0004/Q-001`, whether a move is datable like a spend or fixed like income, answered option A with the stakeholder's words quoted in `refinement-qa.md` and propagated into AC1 and AC6–AC8; *what verification found* — thirteen passes, seven ADRs conforming, nineteen entries disposed, no defect. Nothing in that account came from this conversation.)
  - `claims-are-sourced` → **pass** (`lint-claims --context work-item --changed-since main` → exit 0. The **scope** it printed: *1 document(s) in 1 path(s) differ from main (4c11b04) under docs; citations: every markdown file in the workspace.* That one document is `ADR-0006`, the one this change actually repaired, so the window contained the thing at risk rather than being empty. The six-claim audit in `review.md` is the read behind the gate.)
  - `cross-answer-consistency` → **pass** (`lint-answers --context work-item --changed-since main` → exit 0, *21 consumed human answer(s) and 0 delegation(s) spent*. The `**Cross-answer check:**` bullet above is the read; this execution consumed no answer of its own.)
  - `epic-sign-off` → **pass** ((not applicable in substance)** — `check-epic-signoff WI-0004` → exit 0: *WI-0004 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only.* `engagement-state EP-001` reports `active` with three items still in flight, so no ending is due and none was taken.)
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/review.md` (new)
  - `tracker/items/WI-0004/item.md` — `outcome: delivered`, written by this transition
  - no bug item filed; no question filed; no file under `docs/` written
  - the merge commit is not named here because it does not exist yet: `scripts/record-merge` puts
    it in `item.md` once the real merge has happened
- **Status:** `in-review` → `done`
- **Result:** `WI-0004` is accepted and closed as `delivered`. Thirteen criteria settled with
  evidence, no unrequested scope in the diff, seven binding ADRs conforming and the list complete
  by exhaustion, nineteen invalidation entries confirmed plus the two documents the set does not
  name read and found untouched, seven gaps accepted and every one disposed somewhere the
  orchestrator can see. 119 tests green on the merge result with `main` unmoved. `EP-001` stays
  `open`; closing this item is what makes `WI-0003` runnable.
