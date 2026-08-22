# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-22T01:37:56Z — intake v0.2.0 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly on the stakeholder's stated idea (`IDEA.md`); this skill is not dispatched by `next`
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement, in their own words
  - `tracker/project.yaml`
  - `tracker/items/` — empty at the start of this execution, so `EP-001` and `WI-0001` were the first IDs allocated
  - `docs/product/vision.md` — did not exist; created by this execution
- **Decisions:**
  - See `EP-001`'s entry for how the work was split and why this item is one of three; that reasoning belongs to the split, not to this item.
  - Dependency for this item: `WI-0001` — there is nothing to compute a balance over until expenses are recorded.
  - Acceptance criteria here are deliberately incomplete and are marked so in `## Notes`. They state observable behaviour where the stakeholder's words settle it, and stop where they do not. Padding them into something that looks finished would hand `refine` a polished guess instead of an honest gap.
  - No command names, file formats or data structures appear in the story or the criteria, because the stakeholder named none. "A command" is used on purpose.
- **Questions raised:** none on this item; `EP-001/Q-003` (repayments) decides whether its report must net off settlements
- **Commands:**
  - `scripts/new-item --id WI-0002 --type work-item --epic EP-001 ...` → exit 0, created at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0, reported at the end of this intake — see `EP-001`'s entry for the run)
  - `epic-has-success-measures` → **pass** (assessed on `EP-001`; four measures, each checkable by running the tool — see that item's entry)
  - `items-are-separable` (advisory) → **pass** — WI-0002's dependency is stated above and it delivers something observable on its own: show who owes whom
  - `no-solution-in-the-problem` (advisory) → **pass** — the story and criteria name no technology the stakeholder did not. Python and CSV appear only where they were stated; nothing was removed.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (new)
  - `tracker/items/WI-0002/journal.md`, `tracker/items/WI-0002/history.md` (new, headers written by `new-item`)
- **Status:** `—` → `draft`
- **Result:** Created at `draft` as one of three items under `EP-001`. It is not Ready: `refine` must close the gaps listed in its `## Notes`.

## 2026-08-22T02:42:04Z — refine v0.1.2 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` as the highest-ranked runnable item (priority rank 2, created 2026-08-22T01:34:55Z; BUG-0001 rejected on rank 3, WI-0003 rejected on an unfinished `depends-on`)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md` (one row — created by `intake`, never sent back from a later stage, so this is a fresh refinement and not a defect fix), `journal.md`, and `artifacts/` (empty)
  - `tracker/items/WI-0001/item.md` — the delivered store this item computes over, and its refinement's nine recorded assumptions
  - `tracker/items/WI-0003/item.md` — checked for scope this item might already own; it does not, the two are cleanly separated
  - `tracker/items/EP-001/item.md` and `questions/Q-002.md`
  - `docs/product/vision.md` v3 — checked for contradiction with what is asked here; none. The vision's "so that the group can settle up" is quoted in `Q-001`'s recommendation
  - `docs/architecture/adr/ADR-0001` (repayments are their own record), `ADR-0002` (amount format; payer absorbs the remainder), `ADR-0004` (integer minor units)
  - `expenses/cli.py` — read only far enough to confirm the delivered command shape and that no debt computation exists yet
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`
- **Decisions:**
  - **No acceptance criterion was rewritten.** AC1's unstated choice — pairwise debts or minimised transfers — cascades into AC2, AC4, AC5 and AC6, so rewriting any of them now would be writing down a guess and calling it a requirement. They stand exactly as `intake` left them until `Q-001` is answered.
  - **One question, not a batch.** Everything else `item.md`'s `## Notes` handed to `refine` was either already settled by WI-0001's refinement or small enough to decide here. Six such decisions are recorded in `## Notes` and in `artifacts/refinement-qa.md` with the reason each was judged too small for a round trip: exact summation of printed amounts (which settles the Notes' second bullet, how rounding is *presented*), non-zero debts only, no "settled" versus "never owed" distinction, ordering by debtor then creditor name under WI-0001 AC1's matching rule, debt lines only with no summary, and a person involved in nothing producing no line. Five of the six hold identically under either option in `Q-001`; the third is the only one a stakeholder is likely to have a view on and is the cheapest to reverse.
  - The Notes' **third** bullet — how a repayment that overshoots a debt is presented — needed no question: AC5 as written already states it turns into the other person owing, and assumptions 1 and 2 fix what is printed. Recorded as closed rather than left hanging.
  - `Q-001` was written with a worked three-person example printing both outputs side by side, because the two options differ in what a person sees rather than in anything abstract, and a stakeholder cannot choose between "pairwise" and "minimised" as words.
  - Scope was left as `intake` wrote it; three exclusions already stand and none of this execution's decisions removed one.
- **Questions raised:** `Q-001` (`addressed-to: human`, blocking) — does the report print every debt between each pair, or the shortest list of payments that settles everybody up? Pointer: `artifacts/refinement-qa.md`, round 1, `[unresolved]`.
- **Commands:**
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 0, at the start of this execution
  - `.claude/agile-skills/scripts/validate-workspace .` → exit 1 after the question file was written, reporting `question.blocking.not-suspended` and `board.stale` — both are this execution's own unfinished business, resolved by this transition and by the `board-gen` that follows it
- **Gates:**
  - `workspace-valid` → **pass** — exit 0 before the execution's writes; the two errors seen mid-execution are the suspension this transition performs and the board this execution regenerates, and both clear on it
  - `definition-of-ready` → **fail**, per criterion: R1 pass (frontmatter complete; `type`, `epic`, `priority` set). R2 pass (role "a member of a friend group with a pile of shared expenses recorded", capability "ask the tool who owes whom", outcome "so that we can settle up without anyone reconstructing the arithmetic by hand"). R3 pass (AC1–AC6, labelled, checkboxes). **R4 fail** on AC1 (does not say *which* set of debts — pairwise or minimised), AC2 ("each person's net position in the output" is undefined until the output's shape is), AC4 (deterministic, but the order itself is unnamed — now supplied by assumption 4), AC5 (how an overshooting repayment prints depends on the shape), AC6 (what "reports that nobody owes anybody" replaces depends on the shape); no criterion contains an unmeasurable adjective, so R4's second clause holds. R5 pass (three exclusions; "recording a repayment — that is WI-0001" is one a reader could reasonably assume is included). R6 fail as of this execution — `Q-001` is blocking, which is the point of the suspension. R7 pass (`depends-on: WI-0001`, status `done`). R8 pass (`artifacts/refinement-qa.md` written, every line tagged; nothing tagged `[human]`, because nothing has been). R9 pass (one coherent change: compute debts from the existing store and print them). **R10 fail** — two combinations are unsettled and both are `Q-001`'s: a repayment between two people who share no expense, and a circular set of debts. The full combination table is in `## Notes`, with each row's settlement named
  - `criteria-are-decidable` → **fail** — AC3 is decidable as written (run the report with nothing recorded; expect a line saying so and exit 0). AC1, AC2, AC4, AC5 and AC6 are not: for each of them two implementations that print different lines would both pass. Named criterion by criterion under `definition-of-ready` above
  - `qa-recorded-verbatim` → **pass** — `artifacts/refinement-qa.md` records the question asked, tagged `[refine]`, and its unanswered state, tagged `[unresolved]`. There is nothing tagged `[human]` and nothing has been paraphrased into agreement; the stakeholder has said nothing on this item
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` (new)
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (new)
  - `tracker/items/WI-0002/item.md` — `## Notes` gains the DoR assessment, the six decisions, and the R10 combination table. **Acceptance criteria untouched**
- **Status:** `draft` → `awaiting-answer`
- **Result:** Not Ready, and not overridden — the item genuinely is not Ready and there is nothing to override. One question is open to the stakeholder: pairwise debts, or the shortest list of payments that settles everybody. Everything else this item needed is now settled and written down, so when the answer arrives `answer-questions` can rewrite the criteria and the item should reach Ready in one more pass.

## 2026-08-22T02:50:57Z — answer-questions v0.1.4 — architect

- **Item:** WI-0002
- **Trigger:** `awaiting-answer` since 2026-08-22T02:42:04Z; the stakeholder filled in `## Answer` on `Q-001` between turns, which makes it answerable under the skill's precondition 1 (open, `addressed-to: human`, answer present). Dispatched by the harness ahead of `next`, because `next` step 3 stops on any open human-addressed question and would never reach a step that consumes one.
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` — the only question on this item; answered "A — the pairwise breakdown"
  - `tracker/items/WI-0002/item.md` — the six acceptance criteria, the three open `## Notes` bullets, the six decisions `refine` took without asking, and the R10 table
  - `tracker/items/WI-0002/history.md` — the suspending row of 2026-08-22T02:42:04Z carries `resume-to: draft`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — round 1 as filed, unanswered
  - `docs/architecture/adr/ADR-0001` … `ADR-0005` — checked for contradiction; none contradicts a pairwise report. `ADR-0002` (equal split, payer absorbs the remainder) and `ADR-0004` (integer minor units) are the two the computation rests on, and both are neutral between the options `Q-001` offered
  - `docs/architecture/overview.md` v3 — the module split; no change needed, WI-0002 has no code yet
  - `docs/product/vision.md`, `.claude/agile-skills/spec/question.md`, `.claude/agile-skills/spec/doc-header.md`
  - no `artifacts/plan.md` exists — the item has never been planned
- **Decisions:**
  - **Q-001 — route: the human answered an escalation; propagated, not re-decided.** They chose option **A**, the pairwise ledger, over `refine`'s recommendation of B, and gave traceability as the reason: any line must trace back to what those two people actually shared. Recorded verbatim.
  - **Recorded as `ADR-0006` rather than only in the item.** The answer fixes how the report is computed, which `plan` and `implement` will read from `docs/architecture/adr/` and not from a question file. The ADR states the five computation steps, and states explicitly that a printed circle of debts (A ⟶ B ⟶ C ⟶ A) is **correct output**, so no later skill "fixes" it as a defect.
  - **AC1 amended; AC2–AC6 left alone.** AC1 said "a set of debts" and did not say which set — that is precisely what was asked and answered, so it now says pairwise. The item is at `draft`, so criteria are not frozen and this is a legitimate edit rather than reshaping a target around an arrow; it is called out here because amending a criterion is journalled explicitly whatever the status. The other five become decidable as written once AC1 is concrete, and rewording them belongs to the `refine` execution that owes the R4 and R10 verdict.
  - **No Definition of Ready verdict given.** `answer-questions` does not assess a DoR it did not run; the item goes back to `draft` for `refine`, not forward to `ready`.
  - **Two R10 rows settled from the answer.** "a repayment between two people who share no expense" now prints the debt the other way round; "a circular set of debts" now prints the circle. Both follow from the pairwise rule and neither needed a new decision.
- **Questions raised:** none
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → 2026-08-22T02:48:51Z
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1 (five `claim.citation.unresolved` on the new ADR: a source marker naming an item plus a section and an assumption number — "WI-0002, hash-hash Notes, assumption 1" — is not one of the citation forms `spec/doc-header.md` can resolve, and nor is one naming a question plus a section. Rewritten to the plain item and question forms, which resolve). Note for the toolkit owner: a journal entry that *quotes* an unresolvable marker fails the same gate, so this line describes the offending forms in prose rather than reproducing them
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 5 items, 8 documents
- **Gates:**
  - `answer-is-propagated` → **pass** — every file named in `Q-001`'s `## Consequences` was opened after writing and the change confirmed present: `ADR-0006` exists as a v1 current ADR with the decision and the stakeholder's words; `item.md` AC1 reads "pairwise" and the two R10 rows cite `ADR-0006`; `refinement-qa.md` round 1 carries the `[human]` line verbatim; `history.md` and `journal.md` carry this execution
  - `answered-from-the-record` → **pass** — the answer is the stakeholder's own, quoted from `Q-001` `## Answer`, and the derived computation is cited to `ADR-0002`, `ADR-0004` and `ADR-0001` in `ADR-0006`. Nothing here was inferred from a silent record
  - `escalation-is-justified` → **skipped** — nothing was escalated. The one question on this item came back answered
  - `workspace-valid` → **pass** — `validate-workspace` exit 0 after the transition and `board-gen`
  - `item-resumed-correctly` → **pass** — the suspending row of 2026-08-22T02:42:04Z records `resume-to: draft`; this execution's row targets `draft`
- **Artifacts:**
  - `docs/architecture/adr/ADR-0006-the-debt-report-is-the-pairwise-ledger.md` — created, v1, current
  - `tracker/items/WI-0002/item.md` — AC1 amended; first `## Notes` bullet struck through as settled; two R10 rows resolved; `### Q-001 answered by the stakeholder` section added
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — round 1 answered, banner and DoR section restated
  - `tracker/items/WI-0002/questions/Q-001.md` — `status: answered`, `answered-by: human`, `answered-at: 2026-08-22T02:48:51Z`, four files named under `## Consequences`
  - a commit of the tracker and docs files this execution wrote
- **Result:** The stakeholder chose the pairwise debt report over the minimised settlement, for traceability; it is now `ADR-0006` and AC1 says so, and the two R10 combinations that hung on the choice are settled. WI-0002 is back at `draft` with no open question, and the next `refine` execution owes it a Definition of Ready verdict.
- **Status:** `awaiting-answer` → `draft`

## 2026-08-22T02:59:22Z — refine v0.1.2 — product-analyst

- **Item:** WI-0002
- **Trigger:** `draft`, dispatched by `next` — the highest-ranked runnable item (priority `high`, rank 2) ahead of BUG-0001 (`ready`, `medium`, rank 3); WI-0003 was not runnable (`depends-on: WI-0002`, not `done`).
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — six inherited criteria, three `## Notes` bullets, `refine`'s six round-1 decisions, the R10 table
  - `tracker/items/WI-0002/history.md` — three rows; the item reached `draft` from `awaiting-answer`, not from a send-back by `verify` or `review-close`, so this is a continuation of round 1 and not a defect-driven re-refinement
  - `tracker/items/WI-0002/journal.md` — round 1's entry, and `answer-questions`' entry of 2026-08-22T02:50:57Z
  - `tracker/items/WI-0002/questions/Q-001.md` — answered: option A, the pairwise ledger
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — round 1 as recorded
  - `docs/architecture/adr/ADR-0006` (v1) — the pairwise rule and its five computation steps; `ADR-0002` (v1) — equal split, payer absorbs the remainder; `ADR-0004` (v1) — integer minor units; `ADR-0001` (v1) — a repayment is its own record
  - `docs/architecture/overview.md` v3 — the command list, the exit codes, and that `--file` is global and must precede the subcommand; `expenses/cli.py` — the wording of the existing empty-list messages, read for AC4's exact string
  - `.claude/agile-skills/spec/dor-dod.md` §1 — the ten criteria this execution is judged against
  - `docs/product/vision.md`
- **Decisions:**
  - **Nothing was put to the stakeholder this round.** `refine` may ask directly and the stakeholder is asynchronous, so a question would have meant filing an artifact and stopping the loop. After `Q-001`'s answer, every remaining gap was either arithmetic following from `ADR-0002`, `ADR-0004` and `ADR-0006`, or presentation that `refine` is entitled to decide and record. Filing a question with nothing genuinely undecidable in it would have cost a round trip for nothing, and there is already an outstanding request to the stakeholder on WI-0003.
  - **All six inherited criteria were rewritten, and became eleven.** Four now carry a complete ledger — the `add-person` / `add-expense` / `repay` commands that build it — and the exact stdout it must produce (AC2, AC6, AC8, AC9, AC10, AC11). AC3 states the balance identity as arithmetic a reader can perform by hand rather than as the word "balance". AC5 names the comparison, `name.strip().casefold()`, instead of saying "deterministic". The old-to-new map is in `item.md`.
  - **One inherited criterion was not merely vague but wrong, and the pairwise answer is what exposed it.** Old AC3 announced "nobody owes anybody" when *every person's net position is zero*. That is equivalent to "nothing to print" under the minimised report `refine` had recommended, and **not** equivalent under the pairwise report the stakeholder chose: a circle of equal debts has every net position at zero and three lines that must still print. AC4 now triggers on "no **pair** has a non-zero balance" and AC8 pins the circle down with a worked example. Resolving a contradiction between two criteria is `refine`'s job; it removes nothing the stakeholder asked for.
  - **Three presentation decisions, all reversible, recorded in `item.md` and in the Q&A rather than only here:** the command is `debts` (R4 cannot pass without naming what a reader types; `people`, `expenses` and `repayments` are the existing idiom); the empty line is exactly `Nobody owes anybody.` (an exact string is what makes AC4 decidable; the wording is `refine`'s, not the stakeholder's, and is marked as such); and AC4's trigger is pairs rather than net positions.
  - **Three exclusions added to `## Out of scope`** (R5): suggesting the fewest transfers — the option the stakeholder explicitly rejected, and a separate command over the same data if ever wanted; a per-person summary or totals line; and any per-line explanation of which expenses make up an amount. The traceability they asked for is that a line *can* be reconciled by hand against `expenses`, not that the tool does it.
  - **The R10 table was re-stated against the new numbering** and grew from nine rows to fourteen: the three repayment magnitudes are now separate rows, the circle and the stranger-repayment rows point at criteria rather than at an ADR alone, and a row records that this item introduces no option of its own — which is why the table is short.
- **Questions raised:** none. `artifacts/refinement-qa.md` records both rounds; round 1's single question is `Q-001`, answered by the stakeholder; round 2 asked nothing. No answer is left `[unresolved]`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, run after each edit to `item.md` and to `refinement-qa.md` (5 items, 9 documents)
  - `grep -n "NO_PEOPLE\|NO_EXPENSES\|NO_REPAYMENTS" expenses/cli.py` → `No people recorded.` / `No expenses recorded.` / `No repayments recorded.`, the wording AC4's exact string was matched to
  - `grep -rn -i "nobody owes" tracker/ IDEA.md docs/product/vision.md` → one hit, in `EP-001/Q-003`'s own text and not in anything the stakeholder wrote. A draft sentence in `item.md` attributing the phrase to them was corrected before this entry was written
  - `python3 .claude/agile-skills/scripts/board-gen .` → board regenerated
  - `python3 .claude/agile-skills/scripts/transition WI-0002 --to ready --actor refine …` → the row was written and the journal entry was **refused**: the body was missing the `**Commands:**` bullet this list now supplies, so the entry was appended separately with `scripts/journal-entry`. Worth reporting to the toolkit owner — the two halves of one checkpoint can end up in different states, and `spec/skill-contract.md` §2.3 calls the transition a checkpoint precisely to avoid that
- **Gates:**
  - `workspace-valid` → **pass** — `validate-workspace` exit 0 after each edit and after the transition
  - `definition-of-ready` → **pass**, criterion by criterion, no override: R1 pass (frontmatter complete; `type`, `epic`, `priority` set). R2 pass (role, capability and a "so that" outcome). R3 pass (AC1–AC11, all checkboxes). **R4 fail on all six inherited criteria → rewritten into eleven → pass**: every one now names a command and an output, six carry exact expected stdout, and none contains an adjective without a threshold. R5 pass (six exclusions, three added here). R6 pass (`Q-001` answered; no open question). R7 pass (`depends-on: WI-0001`, `done`). R8 pass (`refinement-qa.md` carries both rounds with `[human]`, `[assumed]` and `[refine]` tags). R9 pass (one command over existing data, no new storage, no new option). **R10 fail → pass** against the fourteen-row table, every row landing on a criterion, an ADR, or an explicit statement that WI-0001 already fixes it
  - `criteria-are-decidable` → **pass** — the test applied to each in turn: AC1, AC2, AC6, AC8, AC9, AC10, AC11 are settled by building the stated ledger and diffing stdout; AC3 by computing the identity from the ledger and comparing to the printed lines; AC4 by the empty and squared-up ledgers with the exact string; AC5 by sorting the printed pairs and by running the command twice; AC7 by AC6's ledger with the remaining debts repaid. A reader with a terminal and no context reaches the same verdict on each
  - `qa-recorded-verbatim` → **pass** — the stakeholder's answer to `Q-001` is quoted word for word in `refinement-qa.md` and in `item.md`; the four round-2 decisions are tagged `[assumed]` and attributed to `refine`, not to them; the one phrase that might read as theirs — `Nobody owes anybody.` — is explicitly recorded as `refine`'s wording
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — acceptance criteria rewritten AC1–AC11; `## Out of scope` extended by three; R10 table re-stated; three new `## Notes` sections — the DoR verdict, the renumbering map, and this execution's three decisions
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — round 2 recorded, the correction to old AC3 written out, the decided-not-asked table, and the Ready verdict with no `## Override`
  - `tracker/board.md` — regenerated
  - a commit of the tracker files this execution wrote
- **Result:** WI-0002 is Ready, without an override. The stakeholder's pairwise answer turned six property-shaped criteria into eleven observable ones, six of which carry a ledger and the exact output it must produce — and it exposed a real contradiction in the inherited "nobody owes anybody" criterion, which announced an empty report for a circle of debts that must in fact print three lines.
- **Status:** `draft` → `ready`

## 2026-08-22T03:07:28Z — plan v0.2.0 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next` as the highest-ranked runnable item (priority-rank 2; BUG-0001 rank 3, WI-0003 blocked on this item)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the eleven acceptance criteria, the `## Notes` sections carrying `refine`'s nine recorded decisions and the R10 combination table
  - `tracker/items/WI-0002/history.md` and `tracker/items/WI-0002/artifacts/refinement-qa.md` — the four `[assumed]` entries from the second refinement round
  - `docs/architecture/overview.md` v3 — the three-module split, the dependency direction, the command list, the exit codes
  - `ADR-0002` (amount format; the payer absorbs the remainder), `ADR-0004` (integer minor units; the `divmod` restatement), `ADR-0006` (the pairwise report and its five steps), `ADR-0001` (repayments are their own record), `ADR-0003` (the JSON ledger), `ADR-0005` (no third-party dependencies)
  - `tracker/project.yaml` — trunk, test and lint commands
  - `tracker/items/WI-0001/artifacts/plan.md` — the mapping-table and assumption conventions this plan follows
  - source: `expenses/cli.py`, `expenses/model.py`, `expenses/store.py`, `tests/cli_harness.py`, `tests/test_cli_repayments.py`
- **Decisions:**
  - **The computation lives in a new module `expenses/debts.py`, as a pure function over a `Ledger`** — *decided*, `ADR-0008`. The alternatives were a handler inside `cli.py` and methods on `Ledger`; both were rejected because AC3 is an arithmetic identity that has to be assertable without going through `argparse` and captured stdout, and because `model.py` is the module WI-0003's importer is meant to reuse as validators. Reversible: one file, one caller.
  - **An uneven split whose payer is not among the sharers leaves the remainder owed by nobody** — *decided*, `ADR-0009`. The record disagreed with itself here: `ADR-0004` says both "the payer is owed `t`" and "the sum of what is owed is `t - remainder`", and WI-0002's R10 table takes the first half while AC3's closing assertion (net positions sum to zero) only holds under the second. Answered from the documents rather than escalated — it is arithmetic, not intent, `ADR-0002` already delegated the odd cent to the architect, and the alternative is `ADR-0002`'s rejected option D reintroduced for one case. `ADR-0009` also records the reading of AC3's "P's share" that this forces.
  - **The pair accumulator holds one signed integer per unordered pair** — *assumed*, plan `## Assumptions` and step 1.2. It makes netting addition, makes AC6's direction reversal fall out of the sign, and makes AC7's "never a `0.00` line" one comparison. Reversible: internal to one function.
  - **Four small behaviours recorded as reversible assumptions rather than ADRs:** no header or summary in the output; an expense with an empty sharer list contributes nothing rather than raising `ZeroDivisionError` on a hand-edited ledger; a name on a record but not in `people` prints in the form the record carries; `debts` is registered last in `--help`.
  - **Followed without re-deciding:** `ADR-0006`'s five computation steps (they are steps 1.1–1.5 of the plan), `ADR-0002` and `ADR-0004`'s remainder rule, `ADR-0005`'s standard-library-only constraint, and `refine`'s three recorded decisions — the command name `debts`, the exact string `Nobody owes anybody.`, and the debtor-then-creditor ordering — all of which are now acceptance criteria.
- **Questions raised:** none. Nothing this plan needed was irreversible or depended on intent no document records; the one contradiction in the record was resolvable from `ADR-0002` and `ADR-0004`, and is recorded as `ADR-0009` so the resolution is findable from the criterion.
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, 83 tests, OK
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 5 items, 11 documents, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0, board already current
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings)
  - `every-criterion-is-addressed` → **pass** — all eleven criteria map to a step and to a named demonstration in `plan.md`'s `## Acceptance criteria mapping`:

    | AC | steps | demonstrated by |
    |----|-------|-----------------|
    | AC1 | 1, 3, 4 | `tests/test_cli_debts.py` — form of each line, exit 0, ledger bytes unchanged |
    | AC2 | 1, 3, 4 | exact three-line output of the worked ledger |
    | AC3 | 1, 2 | `tests/test_debts.py` — per-person signed line-total equals a net position recomputed inline, over every ledger the file builds |
    | AC4 | 1, 3, 4 | three empty-report cases, each asserting the single exact line and exit 0 |
    | AC5 | 1, 4 | mixed-case ledger ordered by case-folded name, printed in first-typed form; two runs byte-identical |
    | AC6 | 1, 3, 4 | exact two-line output after the two repayments |
    | AC7 | 1, 4 | fully repaid ledger → the empty-report line, and `"0.00" not in out` |
    | AC8 | 1, 4 | exact three-line circle, plus a `test_debts.py` assertion that every net position is 0 |
    | AC9 | 1, 2, 4 | exact `3.33`/`3.33` output, plus the `ADR-0009` non-sharing-payer variant |
    | AC10 | 1, 3, 4 | exact reversed line from a lone repayment |
    | AC11 | 1, 4 | three people with nothing recorded → the empty-report line; a fourth uninvolved person changes nothing |

  - `project-commands-resolved` → **pass** — `commands.test` and `commands.lint` were already set for WI-0001 and both were run in this project during this execution: test → exit 0 with 83 tests, lint → exit 0. `commands.build` stays `null`, which `ADR-0005` records as correct for a package run from the checkout.
  - `decisions-recorded` → **pass** — two ADRs (`ADR-0008`, `ADR-0009`), four reversible assumptions each stating what reversing costs, and a `## Decisions and ADRs` table separating what was decided here from what was inherited.
  - `plan-is-executable-without-you` (advisory) → **pass** — five numbered steps, each naming the files it touches and what is true afterwards; step 1 gives the algorithm as five sub-steps and the module's two exported signatures, without writing the implementation.
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` → exit 0). Two citation markers had to be rewritten first: the linter reads a second `src:` inside one marker as part of the citation text, so several sources must be separated by `;` alone.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` — created
  - `docs/architecture/adr/ADR-0008-the-debt-computation-is-a-pure-module.md` — created
  - `docs/architecture/adr/ADR-0009-an-uneven-split-whose-payer-does-not-share-leaves-the-remainder-owed-by-nobody.md` — created
  - `docs/architecture/overview.md` — v3 → v4: the fourth module, the `debts` command, the new dependency edge, and a note that the module is planned rather than built
  - commit of the above, `refs WI-0002`
- **Result:** WI-0002 is planned. One new module holds `ADR-0006`'s five steps as a pure function; `cli.py` gains a `debts` subcommand that only prints. The one thing that made the item hard was not the arithmetic but a contradiction inside the record about where an uneven split's remainder goes when the payer is not a sharer — `ADR-0009` settles it, and names the reading of AC3 that follows, so `verify` does not have to choose between two criteria.
- **Status:** `ready` → `planned`

## 2026-08-22T03:08:06Z — implement v0.2.1 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`, dispatched by `next`; no `wi/WI-0002` branch existed, so this is a fresh start rather than a resumption [src: run: `git branch --list` → `main`, `wi/WI-0001` only]
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the eleven acceptance criteria and the six worked ledgers with exact expected output
  - `tracker/items/WI-0002/artifacts/plan.md` — five steps, the `debts()` algorithm as five sub-steps, the AC mapping table, four assumptions
  - `tracker/items/WI-0002/history.md` — four rows, the last being `ready → planned`; no send-back from `verifying` or `in-review`, so there is no defect to work
  - `tracker/items/WI-0002/questions/Q-001.md` — `answered`, propagated into `ADR-0006` and AC1 before this execution
  - `ADR-0002`, `ADR-0004`, `ADR-0006`, `ADR-0008`, `ADR-0009`, `docs/architecture/overview.md` v4
  - `tracker/project.yaml` — branch prefix `wi/`, commit subject convention, test and lint commands both non-null
  - source: `expenses/cli.py`, `expenses/model.py`, `expenses/store.py`, `tests/cli_harness.py`
- **Decisions:**
  - none yet — this entry opens the execution. Branch `wi/WI-0002` created from `main` at `1fc67eb`.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → exit 0
- **Gates:**
  - `tests-pass` → **not yet run** (no code written)
  - `lint-clean` → **not yet run**
  - `workspace-valid` → **not yet run**
  - `every-criterion-has-a-test` → **not yet run**
  - `commits-reference-the-item` → **not yet run** (no commits on the branch)
  - `no-unplanned-scope` (advisory) → **not yet run**
  - `claims-are-sourced` → **not yet run**
- **Artifacts:**
  - branch `wi/WI-0002`, no commits yet
- **Result:** Implementation of WI-0002 has started on a fresh branch off `main`. The plan's five steps are unstarted; the closing entry will report the work.
- **Status:** `planned` → `in-progress`

## 2026-08-22T03:13:29Z — implement v0.2.1 — developer

- **Item:** WI-0002
- **Trigger:** continuation of this execution — the opening entry at 03:08:06Z created the branch and moved the item to `in-progress`; this entry reports the work
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `artifacts/plan.md`, `history.md`, `questions/Q-001.md` (answered, already propagated)
  - `ADR-0002`, `ADR-0004`, `ADR-0006`, `ADR-0008`, `ADR-0009`, `docs/architecture/overview.md` v4
  - source, to orient: `expenses/cli.py`, `expenses/model.py`, `expenses/store.py`, `tests/cli_harness.py`, `tests/test_cli_repayments.py`
- **Decisions:** all inside the plan's latitude.
  - **`_display_names` walks people, then expenses, then repayments, with `dict.setdefault`.** The plan said "first occurrence winning" without saying what to iterate. No criterion reaches the fallback; it exists so a hand-edited ledger reports instead of raising `KeyError`.
  - **`cli.py` imports the module as `debts_module`.** The subparser variable inside `build_parser` is called `debts`, which is the plan's own wording, so the import is what got renamed.
  - **Three ledgers were added to `tests/test_debts.py` beyond the ones the criteria name** — `NON_SHARING_PAYER`, `NO_SHARERS` and `MIXED_CASE`. Each is a case `plan` recorded as an assumption or an ADR (`ADR-0009`, plan assumptions 2 and 3), and each is registered in `LEDGERS`, so AC3's balance identity runs over it too.
  - **The two ordering tests were rewritten after being checked by mutation.** The first version used people `cara`, `ANA`, `Ben`, whose display forms happen to sort in the same order as their case-folded forms, so it would have passed against a sort on the display names. `ana`/`Ben`/`Cara` discriminates, and the mutation confirms it.
  - **Decided *not* to fix `expenses/cli.py`'s module docstring**, which still claims `cli.py` is "the only one that exits" — false since `main` returns an `int`, and already corrected in the overview by `review-close`'s D12 audit. It traces to no criterion of this item, so it is recorded in `impl-report.md` under `## What I did not do` rather than fixed here.
- **Questions raised:** none. Nothing in the plan turned out to be silent on a decision that was not the developer's to make; `ADR-0009` had already settled the one place the record disagreed with itself.
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → exit 0
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, 97 tests, OK (after step 2)
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, 115 tests, OK (branch head)
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 -m expenses --file /tmp/x.json debts` → exit 0, printed `Nobody owes anybody.` (step 3's stated observable)
  - mutation check, sort keyed on the display names → exit 1, FAILED (failures=2)
  - mutation check, repayments ignored → exit 1, FAILED (failures=11)
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, all 2 commits name WI-0002
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0
- **Gates:** all run on the branch head at `1d47123`, after the last change.
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` → exit 0, 115 tests, OK; 83 before this item)
  - `lint-clean` → **pass** (`python3 -m compileall -q expenses tests` → exit 0; a syntax check only, per `ADR-0005`)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 5 items, 11 documents, 0 errors)
  - `every-criterion-has-a-test` → **pass** — eleven criteria, eleven rows in `impl-report.md`'s evidence table, each naming test functions: AC1 `TestReportShape` ×3 plus `TestBalance.test_no_debt_is_zero_or_negative`; AC2 `test_ac2_three_lines_in_this_order`; AC3 `TestBalance` ×2 over all eleven registered ledgers; AC4 `TestNobodyOwesAnybody` ×3; AC5 `TestOrdering` ×4; AC6 `test_ac6_repayments_net_off_and_an_overshoot_reverses_the_pair`; AC7 `test_ac7_every_debt_repaid_prints_no_zero_line`; AC8 `test_ac8_a_circle_is_printed_not_collapsed` plus the net-positions assertion; AC9 `test_ac9_an_uneven_split_leaves_the_remainder_with_the_payer` plus `test_adr0009_a_non_sharing_payer_absorbs_the_odd_cent`; AC10 `test_ac10_a_repayment_between_people_who_share_nothing_reverses`; AC11 `test_ac11_people_with_nothing_recorded` plus `test_ac11_an_uninvolved_person_neither_adds_a_line_nor_removes_one`
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0002 wi/WI-0002` → exit 0)
  - `no-unplanned-scope` (advisory) → **pass** — `git diff --stat main..wi/WI-0002` is three new files, four hunks in `cli.py` (import, constant, subparser, handler), the overview's v5 edit, and the tracker's own files. No hunk without a plan step behind it
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` → exit 0)
- **Artifacts:**
  - `expenses/debts.py` — new, 93 lines: `Debt`, `_display_names`, `_add`, `debts`
  - `expenses/cli.py` — the `debts` subparser, `NOBODY_OWES`, `cmd_debts`
  - `tests/test_debts.py`, `tests/test_cli_debts.py` — new, 32 new tests between them
  - `docs/architecture/overview.md` — v4 → v5, step 5 of the plan
  - `tracker/items/WI-0002/artifacts/impl-report.md` — new
  - branch `wi/WI-0002`, commits `89a3904..1d47123` (2 commits, `main..wi/WI-0002`)
- **Result:** The `debts` command is built and all eleven acceptance criteria have named tests behind them. The whole suite is green at 115 tests, up from 83. Two of the criteria were checked by mutation rather than trusted: an ordering test that would have passed against the wrong sort key was found and rewritten. Nothing was escalated; `impl-report.md` declares the three things deliberately not done, of which the notable one is `cli.py`'s module docstring, still carrying a claim the overview corrected for WI-0001.
- **Status:** `in-progress` → `verifying`

## 2026-08-22T03:18:12Z — verify v0.1.2 — qa-engineer

- **Item:** WI-0002
- **Trigger:** status `verifying`, dispatched by `next`; `impl-report.md` present and branch `wi/WI-0002` checked out at `c73f039b31bdc676ab6815755d18d3a6ef1f25ab`
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the eleven criteria, read before the implementation report
  - `tracker/items/WI-0002/history.md`, `artifacts/plan.md`, `artifacts/impl-report.md`, `artifacts/refinement-qa.md`
  - `ADR-0002`, `ADR-0004`, `ADR-0006`, `ADR-0008`, `ADR-0009`, `docs/architecture/overview.md` v5
  - `tracker/project.yaml` — the test and lint commands this skill ran itself
  - the code on `wi/WI-0002` at `c73f039`: `expenses/debts.py`, the four `cli.py` hunks, and `git diff main..wi/WI-0002`
- **Decisions:**
  - **Each criterion was settled from the criterion, not from the report.** Thirteen scratch ledgers were built with the real `add-person`, `add-expense` and `repay` commands and the report run against each. `impl-report.md` is cited nowhere in `verify-report.md`'s evidence column.
  - **AC3 was checked with a script written for this verification**, `/tmp/v2/check_ac3.py`, which parses the printed lines back into minor units and recomputes each person's net position from the JSON ledger. It imports nothing from `expenses.debts`, so it does not inherit the arithmetic it is checking. It reported `net sum = 0` and no mismatched person on all thirteen ledgers.
  - **AC5 needed ledgers built specifically to discriminate.** The obvious mixed-case ledger — people `cara`, `ANA`, `Ben` — happens to sort identically by display form and by case-folded form, so it would pass against the wrong sort key. People `ana`/`Ben`/`Cara` (debtor column) and `Ben`/`ana`/`Cara` (creditor column) reverse under a display-form sort, and both came out in case-folded order. `impl-report.md` records the developer hitting and fixing the same trap, which is why this was checked rather than assumed.
  - **Two observations classified as neither send-back nor bug.** `cli.py`'s module docstring still claims the module is "the only one that exits", which is false and which `review-close` already corrected in the overview for WI-0001. It is a comment: no acceptance criterion of any item constrains it and there is nothing to reproduce, so filing a bug would create an item whose verification is "read the file". Recorded in `verify-report.md` under `## Defects found` as an observation. Likewise the two hand-edited-ledger paths in `debts.py`, which are declared in `plan.md` as reversible assumptions and are therefore not undeclared scope.
  - **No criterion was judged ambiguous.** `ADR-0009`, written during planning, is what removed the one candidate — AC3's reading of "P's share" for a payer who is not a sharer. That case was triggered directly (`--payer Ana --amount 10.01 --shared-by Ben --shared-by Cara`) and behaves as the ADR says.
- **Questions raised:** none
- **Commands:** all run by this skill, on the branch head.
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 115 tests`, `OK`
  - `python3 -m compileall -q expenses tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
  - the AC2 ledger built with six commands, then `python3 -m expenses --file /tmp/v2/ac2.json debts` → exit 0, the three expected lines, stderr empty
  - `md5sum` of that ledger before and after the report → `f082a57c44835f2a8acfcffa5221884d` both times
  - `debts` twice into two files, `diff` → identical
  - the AC6, AC7, AC8, AC9, AC10, AC11 ledgers and both ordering ledgers, each followed by `debts` → every output matched the criterion exactly
  - `python3 /tmp/v2/check_ac3.py` over thirteen ledgers → `net sum = 0`, `mismatched people = none`, every time
  - `debts` on a missing file → `Nobody owes anybody.`, exit 0
  - `debts` on `{not json` → `error: … is not valid JSON: …`, exit 1
  - `debts` on a `chmod 000` ledger → `error: cannot read the ledger at …: [Errno 13] Permission denied`, exit 1
  - `python3 -m expenses debts --file …` → `unrecognized arguments`, exit 2
  - `python3 -m expenses --file … debts --all` → `unrecognized arguments`, exit 2
  - `python3 -m expenses --file … add-expense --payer Ana --amount 10.01 --shared-by Ben --shared-by Cara`, then `debts` → `Ben owes Ana 5.00` / `Cara owes Ana 5.00`
  - seven mutations of `debts.py` / `cli.py`, each run through `python3 -m unittest tests.test_debts tests.test_cli_debts` and reverted → failures of 2, 11, 8, 5, 4, 17 and 22 respectively
  - `git diff main..wi/WI-0002` and `git diff --name-only main..wi/WI-0002` → ten files, every hunk traceable to a plan step
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` → exit 0, 115 tests, OK)
  - `lint-clean` → **pass** (`python3 -m compileall -q expenses tests` → exit 0; a syntax check only, per `ADR-0005`)
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 5 items, 11 documents)
  - `every-criterion-independently-checked` → **pass** — eleven rows in `verify-report.md`, each naming a command this skill ran and quoting its actual output; the implementation report is not evidence for any of them
  - `negative-cases-exercised` → **pass** — eight conditions triggered: no file, malformed JSON, unreadable file, people with nothing recorded, everything repaid, `--file` misplaced, an unknown option, and the uneven split whose payer does not share
  - `tests-would-fail-without-the-change` (advisory) → **pass** — seven mutations, every criterion covered by at least one, mapped in `verify-report.md`
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` — created, `Verified-commit: c73f039b31bdc676ab6815755d18d3a6ef1f25ab`
  - `tracker/items/WI-0002/item.md` — all eleven criteria ticked, each against a command in the report
  - no bug items filed
- **Result:** WI-0002 passes verification. All eleven criteria were demonstrated against `c73f039` with commands run here, including an AC3 checker that recomputes the arithmetic from the JSON rather than from the code under test, and eight negative cases triggered rather than read about. Seven mutations confirm the tests bite. One methodology hazard is recorded in the report: a same-length mutation reverted within the same second left a stale `__pycache__` serving mutated bytecode against a clean working tree, which briefly looked like 22 real failures — clearing the caches restored a green suite.
- **Status:** `verifying` → `in-review`

## 2026-08-22T03:27:00Z — review-close v0.3.1 — reviewer

- **Item:** WI-0002
- **Trigger:** status `in-review`, dispatched by `next` as the highest-ranked runnable item (priority rank 2; BUG-0001 rejected on rank 3, WI-0003 rejected on an unfinished `depends-on`)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the eleven criteria and their tick state
  - `tracker/items/WI-0002/history.md` — eight rows, checked for chaining and against `item.md`'s status
  - `tracker/items/WI-0002/journal.md` — all eight entries, read in full
  - `tracker/items/WI-0002/artifacts/plan.md`, `impl-report.md`, `verify-report.md`, `refinement-qa.md`
  - `tracker/items/WI-0002/questions/Q-001.md` — `answered`, four files named under `## Consequences`, each present
  - `git diff main..wi/WI-0002` — read hunk by hunk: `expenses/debts.py` (new), four hunks in `expenses/cli.py`, `tests/test_debts.py` and `tests/test_cli_debts.py` (new), the overview's v5 edit
  - `docs/architecture/adr/ADR-0001`, `ADR-0002`, `ADR-0003`, `ADR-0004`, `ADR-0006`, `ADR-0008`, `ADR-0009`; `docs/architecture/overview.md` v5
  - code the change reaches but does not contain: `expenses/model.py` (`normalise_name`, `format_amount`, `Ledger.from_dict`), `expenses/store.py` (`load`), `expenses/cli.py` (`main`)
  - `.claude/agile-skills/spec/dor-dod.md` §3 and §4, `spec/journal-and-history.md`, `.claude/agile-skills/pipeline.yaml`
- **Decisions:**
  - **Accepted, and the one Definition of Done failure was corrected here rather than sent back.** D12 failed on a single claim: `ADR-0008` wrote "it … raises nothing — every ledger the store can load has a debt report", `implement` copied it into the overview v5 and into `debts.py`'s docstring, and it is false — `Ledger.from_dict` checks that keys exist and not what their values hold, so a hand-edited ledger with a string `amount_minor` loads and then raises `TypeError` out of the share division. Correcting `docs/` is this skill's own gate to enforce and the project's own precedent (overview v3 was `review-close` correcting a false sentence for WI-0001), so the overview went to v6 with a change-log row.
  - **`ADR-0008` left as written.** Superseding a recorded decision is not this skill's to do, and as a statement of design intent — the module defines no error path of its own — the sentence holds. The overview now names where the unqualified wording lives, so a reader who starts at the ADR finds the qualification.
  - **`expenses/debts.py`'s docstring left as written, and accepted as a recorded gap.** Editing source now would put a code commit after the verification and send the item back to `verifying` under D10 for one sentence. The gap is written into `item.md`'s `## Notes`, not only into the review, so it survives the close.
  - **The behaviour behind the false claim is a defect, and it is not this item's.** The same hand-edited ledger crashes the `expenses` and `repayments` listings through `format_amount` at `expenses/cli.py` line 192, and `store.py` documents refusing a mis-shaped file — so value types slipping past `Ledger.from_dict` is a WI-0001 defect. It could not be filed: `pipeline.yaml`'s only `null → ready` transition names `verify` and the only `null → draft` names `intake`, so a bug filed by `review-close` fails `validate-workspace` as an illegal transition. Recorded as finding F2 and in `item.md`'s `## Notes` instead. This skill's SKILL.md tells it to file a bug here, so the contract and the pipeline disagree — reported rather than worked around silently.
  - **No finding against the change itself.** Every hunk maps to a plan step and to a criterion, and none contradicts an ADR. The signed-per-pair accumulator makes AC6's reversal and AC7's "never a `0.00` line" fall out of the arithmetic rather than being special cases, and the ordering tests use names whose display and case-folded forms sort differently, so they bite against the wrong sort key.
  - **The epic stays `open`, and no sign-off question was filed.** BUG-0001 is `ready` and WI-0003 is `draft`, so this was not the epic's last child; DE7 requires the sign-off to be filed *after* the last child closes, and filing it now would be an acceptance of something else.
  - **Merged after closing, not before.** `check-commit-refs` reads `main..wi/WI-0002`, which merging empties.
- **Questions raised:** none
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → 2026-08-22T03:23:54Z
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → exit 0 ("verified at c73f039b; wi/WI-0002 has moved to 9b007eb2 but only the record changed")
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, all 4 commits name WI-0002
  - `git checkout -b trial/WI-0002 main` → exit 0; `git merge --no-ff wi/WI-0002` → exit 0, clean
  - on the merge result: `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 115 tests`, `OK`; `python3 -m compileall -q expenses tests` → exit 0
  - `git checkout wi/WI-0002`; `git branch -D trial/WI-0002` → the trial discarded, nothing published
  - `python3 -m expenses --file /tmp/rc/hand.json debts` on a hand-edited ledger whose `amount_minor` is the string `"3000"` → traceback, `TypeError: unsupported operand type(s) for //: 'str' and 'int'`, exit 1 — the evidence for finding F1
  - `python3 -m expenses --file /tmp/rc/hand.json expenses` → the same `TypeError`, raised at `expenses/cli.py` line 192 through `format_amount` — the evidence that F2 is WI-0001's, not this item's
  - `python3 -m expenses --file … add-expense --payer Ana --amount 10.01 --shared-by Ben --shared-by Cara`, then `debts` → `Ben owes Ana 5.00` / `Cara owes Ana 5.00`, checking `ADR-0009`'s stated consequence against the built code
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, after the overview edit
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 5 items, 11 documents
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0002` → exit 0 (work-item, not an epic)
- **Gates:**
  - `definition-of-done` → **pass on D1–D11, fail on D12, corrected in this execution.** Per criterion, with evidence, in `artifacts/review.md`'s `## Definition of Done` table: D1 eleven ticked checkboxes; D2 eleven evidence rows in `verify-report.md`, none citing `impl-report.md`; D3 gates run at the last code commit `1d47123`, re-run by `verify` at `c73f039` and again here on the merge result; D4 `Q-001` answered; D5 eight rows and eight entries, chaining to `in-review`; D6 `ADR-0008` and `ADR-0009` cited from `plan.md`; D7 overview v4 → v5 with a change-log row; D8 `check-commit-refs` exit 0; D9 trial-merged green and merged after the close; D10 `check-verify-freshness` exit 0; D11 this review, `## What I examined` first; **D12 fail** on one claim of eight audited, corrected as overview v6
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness WI-0002 wi/WI-0002` → exit 0)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0002 wi/WI-0002` → exit 0, 4 commits)
  - `tests-pass-on-the-merge-result` → **pass** — run on the trial merge of `wi/WI-0002` into a throwaway copy of `main`, not on the branch: `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 115 tests`, `OK`. `__pycache__` was cleared first, per the hazard `verify` recorded
  - `workspace-valid` → **pass** (`validate-workspace .` → exit 0, 0 errors, 0 warnings, after the overview and item edits)
  - `record-is-reconstructible` → **pass** — answered from the tracker, `docs/` and `git log` alone: *what was built and why* — one `debts` command over the pairwise ledger the stakeholder chose on `Q-001`, recorded as `ADR-0006`; *which skill decided what* — `refine` the command name, the empty-report string and the pair-based trigger for it, `plan` the pure module (`ADR-0008`) and where an uneven remainder goes when the payer does not share (`ADR-0009`), `implement` four in-plan choices, `verify` nothing; *what questions arose and how they were resolved* — `Q-001`, answered by the stakeholder, propagated into `ADR-0006`, AC1 and the R10 table; *what verification found* — eleven criteria demonstrated with commands `verify` ran itself, eight negative cases triggered, seven mutations, no defect
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` → exit 0, after the v6 edit)
  - `epic-sign-off` → **pass** (`check-epic-signoff WI-0002` → exit 0: the gate applies to epic closure, and WI-0002 is a work-item). `EP-001` is not closing — BUG-0001 and WI-0003 are still open — so no `kind: sign-off` question was filed; DE7 requires it to come after the last child closes
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` (new) — what was examined, the eight-claim D12 audit with what was opened for each, the twelve-criterion Definition of Done table, three findings, five accepted gaps
  - `tracker/items/WI-0002/item.md` — `status: done`, `outcome: delivered`, and a `## Notes` section recording the five accepted gaps
  - `docs/architecture/overview.md` — v5 → v6: the `debts.py` "raises nothing" claim qualified to what the code supports, with a change-log row
  - `tracker/board.md` — regenerated
  - the merge of `wi/WI-0002` into `main`, and a commit of the record this execution wrote
- **Status:** `in-review` → `done`
- **Result:** WI-0002 is delivered and merged: `python3 -m expenses debts` prints the pairwise debts, all eleven criteria ticked against commands `verify` ran itself, 115 tests green on the merge result. The review's one real finding is a documentation failure rather than a behavioural one — three documents said `debts.py` "raises nothing", and a hand-edited ledger with a string amount disproves it; the overview is corrected, the ADR and the module docstring are recorded as accepted gaps, and the defect underneath belongs to WI-0001 and could not be filed as a bug because the pipeline lets only `verify` create one.
