# Journal — WI-0004

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-26T23:47:07Z — answer-questions v0.2.0 — architect

- **Item:** WI-0004
- **Trigger:** not dispatched — this item was created by the `answer-questions` execution on WI-0001, when the stakeholder's answer to `WI-0001/Q-003` implied work no item recorded (`spec/ids-and-statuses.md` §5)
- **Inputs read:**
  - `tracker/items/WI-0001/questions/Q-003.md` — the stakeholder's reply, which is the whole basis for this item
  - `tracker/items/WI-0001/item.md` — what WI-0001 does and does not record, so this item's criteria do not assume a person or an expense can be named in a way WI-0001 has not provided
  - `tracker/items/WI-0002/item.md` — to place the dependency the stakeholder's constraint implies
  - `tracker/items/EP-001/item.md` — the goal and success measures this item was priced against
  - `.claude/agile-skills/spec/ids-and-statuses.md` §5 and §6, `.claude/agile-skills/spec/work-item.md`
- **Decisions:**
  - Scope is **deletion only**. Rationale: the stakeholder was offered correcting and removing together and chose removal — *"being able to delete a mistake matters more to me than editing one"*. Editing is in `## Out of scope` with that quote, so a later reader can tell a decision from an omission.
  - `depends-on: WI-0002`. Rationale: their constraint was *"doesn't need to hold up the who-owes-whom feature"*; the dependency is that sentence made mechanical, and it is recorded in `## Notes` as a scheduling dependency rather than a technical one, because deletion needs only WI-0001's data store.
  - `priority: medium`. Rationale: `spec/ids-and-statuses.md` §6 reserves `high` for what the epic's stated outcome requires, and EP-001's goal and success measures are coherent without deletion.
  - AC3 refuses a deletion that would leave an expense referring to a person who no longer exists. Rationale: WI-0001 already refuses an expense naming an unknown person, so allowing a deletion to create exactly that state would contradict a criterion of the item this one builds on. Whether the rule should instead be "delete the person once their expenses are gone" is flagged in `## Notes` as refinement's.
  - The criteria are written in `intake`'s "a documented command" shape rather than naming commands. Rationale: naming the surface is `refine`'s job on this item, and inventing `person delete` here would pre-empt a refinement that has not happened. `## Acceptance criteria` says so in the item itself, so nobody mistakes a first statement for a refined one.
- **Questions raised:** none — nothing about this item needs the stakeholder before `refine` runs on it
- **Commands:**
  - `scripts/new-item --id WI-0004 --type work-item --title "Delete a person or an expense recorded by mistake" --epic EP-001 --priority medium --status draft --actor answer-questions --arose-from WI-0001/Q-003` → exit 0
- **Gates:** the gates for the execution that created this item are journaled on WI-0001, where the transition was made. As they bear on this item:
  - `answer-is-propagated` → **pass** (this item is itself the propagation of `WI-0001/Q-003`, and it is named in that question's `## Consequences`, in WI-0001's `## Out of scope`, and in EP-001's `## Scope`)
  - `answered-from-the-record` → **pass** (every clause above traces to the stakeholder's verbatim reply or to a cited spec section)
  - `escalation-is-justified` → **skipped** (nothing escalated)
  - `workspace-valid` → **pass** (run by the transition on WI-0001; this entry is what clears `journal.execution.missing` on the creation row below)
  - `item-resumed-correctly` → **skipped** (this item was created, not resumed)
  - `a-deferral-is-not-an-answer` → **skipped** (the reply that produced this item decided its question; it did not defer)
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` (new) — story, four first-statement criteria, out-of-scope and notes
  - `tracker/items/WI-0004/history.md`, `tracker/items/WI-0004/journal.md` (new)
- **Status:** `—` → `draft`
- **Result:** Filed from the stakeholder's answer to WI-0001/Q-003: a mistaken person or expense can be deleted, editing is not wanted, and the work waits behind WI-0002 at their request. It is at `draft` and has its own refinement ahead of it.

## 2026-08-27T00:56:56Z — refine v0.2.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft` — `next` dispatched this skill as the status owner. WI-0004 became runnable this run when its only `depends-on`, WI-0002, reached `done`; it tied BUG-0002 on priority-rank 3 and won on `created` ascending (2026-08-26T23:42:32Z against 2026-08-27T00:16:35Z)
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `history.md` (one row: created by `answer-questions` from `WI-0001/Q-003`), `journal.md`; `artifacts/` held only `.gitkeep` — this is a fresh draft, not a send-back
  - the six answered questions whose answers constrain this item, in full: `WI-0001/Q-003` (deletion wanted, editing refused, timing delegated), `WI-0001/Q-001` (equal split), `WI-0001/Q-002` (description and date), `EP-001/Q-002` (a payment list, not net positions), `EP-001/Q-001` and `EP-001/Q-003`
  - `tracker/items/WI-0001/artifacts/refinement-qa.md` — A1 to A12, and its round-2 "considered asking, and did not" table, which is the precedent this item's D1–D4 rest on
  - `.claude/agile-skills/spec/dor-dod.md` §1; `.claude/agile-skills/spec/question.md` §§1–2
  - **the delivered tool itself**, because the central gap could not be assessed from documents: built a store with the real commands and read back `expense list`, `person list`, `settle` and the stored JSON
- **Decisions:**
  - **One question to the human, and only one.** What deleting a person does to that person's expenses is a product stake on the two counts the procedure names explicitly — it is what happens to their data, and it is irreversible, since they have already ruled out an undo. `Q-001` offers four options: refuse and name the expenses in the way; cascade; delete and leave the expenses; refuse-by-default with an opt-in flag. Recommendation A. Option C is argued **against** rather than offered neutrally, because it is the only one that can make `settle` print a wrong answer without saying so.
  - **The draft AC3 is a guess and was treated as one.** It says deletion is refused when it would leave the data inconsistent — which is option A — but `answer-questions` wrote it when it created the item, not the stakeholder. Building on it would have been exactly the guess the protocol exists to prevent, and the item's own `## Notes` already flagged it as unsettled.
  - **Nine gaps were assessed for ownership and eight were not asked**, each with its reason recorded in the Q&A's table so that "only one question" is auditable rather than asserted. The closest call was how an expense is named on the command line: an expense carries **no identifier at all** today — verified by reading a store built with the delivered commands — so a handle has to be invented and no option changes nothing. Decided here (D2) under WI-0001's A1 precedent, which fixed an entire command surface without asking, and recorded with both rejected alternatives and its stated cost.
  - **One of the three things the item said refinement must settle needed nobody: it was answered by reading.** "Whether deleting an expense that has already been settled means anything" has no answer because there is no such state — `settle` writes nothing and marks nothing as paid (WI-0002 AC5). Recorded as answered-from-the-record, not as assumed.
  - **Four assumptions taken and marked `[assumed — refine, not asked]`:** D1 the command surface (`person delete <NAME>`, `expense delete <NUMBER>`); D2 an expense is named by its 1-based position and `expense list` grows a number column, with the renumbering cost stated; D3 deletion does not prompt, because nothing in this tool is interactive and A2 already fixed its contract; D4 a deletion prints what it deleted. None is reported as the stakeholder's.
  - **R9 passes, and is stated rather than assumed.** Deleting a person and deleting an expense are one command surface, one storage rewrite and one refusal path; splitting them would produce two items that both have to answer Q-001. Not split.
  - **Seven acceptance criteria drafted and deliberately not installed.** AC3 and AC5 depend on the answer. An item whose criteria half-assume a reply is worse than one that still says "a documented command", so they sit in the Q&A for the next execution to install.
  - **No override recorded.** An override waives criteria on the stakeholder's say-so; they have not been asked for one, and naming a criterion they never waived would be a false entry.
- **Questions raised:** 1 — `WI-0004/Q-001`, `addressed-to: human`, `blocking: true`, recorded in `artifacts/refinement-qa.md` under "Round 1". Left `[unresolved]`; it is the reason for the suspension. Its `## Context` opens by saying it is the only question in this round, so the stakeholder is not left waiting for two more (F-020)
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0 on entry; exit 1 twice mid-execution with exactly the two findings this transition resolves (`board.stale`, `question.blocking.not-suspended`)
  - built a scratch store with the delivered commands and read back `python3 -m expenses expense list`, `person list`, `settle`, `python3 -m expenses --help`, and the raw JSON → confirmed an expense record is `{amount_minor, paid_by, shared_by, shares_minor, date, description}` with **no identifier**, and that `expense list` prints no handle. This is the fact D2 turns on, and it was read rather than assumed
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-08-27T00:54:13Z`, the question's `created`
- **Gates:**
  - `workspace-valid` → **pass** (exit 0 on entry, and again after this transition; the two mid-execution errors were the expected consequences of filing a blocking question, and the transition is what clears them)
  - `definition-of-ready` → **fail, per criterion, and not overridden.** R1 pass (frontmatter complete); R2 pass (role, capability, "so that"); R3 pass (AC1–AC4 labelled checkboxes); **R4 fail** — all four criteria say "a documented command", which names nothing, and AC3 turns on the phrase Q-001 is about; R5 pass (editing in place, undo, deleting the whole store); **R6 fail by design** — this execution filed the blocking question that suspends the item; R7 pass (`depends-on: WI-0002`, `done` at 2026-08-27T00:51:47Z); **R8 fail** — `refinement-qa.md` is `status: agenda`, which is the honest value while the conversation has not happened; R9 pass, argued in the Q&A; **R10 fail** — nothing said what `settle` prints after a deletion, what deleting a non-existent thing does, or what renumbering does to the listing. R4, R8 and R10 are what the next execution closes
  - `criteria-are-decidable` → **fail**, which is R4 restated and is why the item is not going to `ready`. Seven replacement criteria are drafted in the Q&A, each naming a command and an exact expected output; five of them are decidable today and two wait on Q-001
  - `qa-recorded-verbatim` → **pass, at `agenda`.** Every stakeholder sentence this item rests on is quoted verbatim from the question that produced it, and nothing is attributed to them that they did not say. The one exchange that has not happened is marked `[unresolved]` rather than anticipated
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-001.md` (new) — the question, four options, a recommendation, and an argument against option C
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` (new, `status: agenda`) — the DoR table, the nine-gap ownership table, D1–D4, the seven drafted criteria, and the not-Ready verdict
  - `tracker/items/WI-0004/item.md` — a `## Notes` subsection recording where refinement got to, so a reader of the item alone finds the agenda
  - commit: `tracker: the refined item and its Q&A record (refs WI-0004)`
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0004 is suspended on one question to the stakeholder: what deleting a person does to that person's expenses. Everything else on the item was closed without them — eight of nine gaps, one of which turned out to be answerable by reading WI-0002's record rather than by deciding anything — and all of it is on disk as an agenda, with seven criteria drafted and two of them waiting on the answer. The item is not Ready and no override was recorded.

## 2026-08-27T01:02:57Z — answer-questions v0.2.0 — architect

- **Item:** WI-0004
- **Trigger:** `awaiting-answer` — the stakeholder replied to the escalated blocking question
  `Q-001` between turns, so `answer-questions` ran ahead of `next` to consume the answer. An
  answered-but-unconsumed human question stops the orchestrator on every subsequent run (F-011),
  so consuming it is the only thing that could have moved this workspace.
- **Inputs read:**
  - `tracker/items/WI-0004/questions/Q-001.md` — the only question on the item, `addressed-to:
    human`, `blocking: true`, with `## Answer` filled in by the stakeholder
  - `tracker/items/WI-0004/item.md` — the four draft criteria and the "Where refinement got to"
    section left by `refine`
  - `tracker/items/WI-0004/history.md` — for the `resume-to` on the suspending row: `draft`
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` v`status: agenda` — the agenda, the
    `[assumed]` decisions D1–D4, and the seven conditional criteria drafted against the answer
  - `docs/architecture/adr/` — all five ADRs listed and ADR-0001, ADR-0005 checked for conflict
    with option A; none contradicts it
  - `tracker/items/WI-0002/artifacts/review.md` (via the citation in the Q&A) — `positions()`
    silently ignoring a name not in `data["people"]`, which is what makes this answer matter
    beyond the `person delete` command
  - `.claude/agile-skills/spec/question.md` §2, §3 — the answer/consequence body rules
- **Decisions:**
  - **Q-001 — what deleting a person does to that person's expenses: option A**, refuse and name
    the expenses in the way. Route: **the human answered an escalation**; this execution decided
    nothing about it and propagated their words. Their reason is on the record with the choice
    because it constrains the implementation, not just the outcome: they bought *"a couple extra
    commands"* against two named harms, so the refusal must say what to delete first.
  - **AC3b added to the drafted criteria** — deleting a person becomes ordinary once nothing
    names them. This is not a new decision; it is option A's other half, and without it an
    implementation that refused every person-deletion would satisfy the drafted AC3. Recorded in
    the Q&A rather than in `item.md`, with the rest.
  - **No ADR written.** The contract wants a new decision recorded as an ADR; this execution took
    no architectural decision. The choice was the stakeholder's, from four options put to them,
    and it is recorded where it was made. Writing an ADR would claim the architect decided
    something the stakeholder decided.
  - **No new item filed.** The answer narrows scope rather than widening it: option D, the bulk
    `--and-their-expenses` flag, was offered and declined, so there is nothing to file under
    `arose-from`. That it was declined is written into the Q&A so a later execution does not add
    it as an obvious convenience.
  - **Criteria not installed in `item.md`.** Installing the eight drafted criteria and judging
    the Definition of Ready is `refine`'s step, and `resume-to` sends the item to `draft` for
    exactly that. Propagation here means putting the answer where `refine` will read it and
    making the stale claims in `item.md` true again — not doing `refine`'s job in passing.
- **Questions raised:** none. No question on any item in this workspace is now open.
- **Commands:**
  - `validate-workspace .` (before propagating) → exit 0, 0 errors, 0 warnings
  - `validate-workspace .` (after propagating) → exit 1: `claim.citation.unresolved` at
    `refinement-qa.md`, from a `[src: ...]` citation whose path I had wrapped in backticks; fixed
    by removing them, the surrounding file already using the unbackticked form
  - `validate-workspace .` (after the fix) → exit 1, with only the two errors this execution's own
    transition and the board regeneration clear: `board.stale`, and `question.awaiting.none-open`
    on WI-0004 (the item is still `awaiting-answer` while its only question is now `answered`)
  - `transition WI-0004 --to draft --actor answer-questions --journal-body-file ...` → exit 1 on
    the first attempt: the body was missing the `**Commands:**` and `**Status:**` bullets, nothing
    was written. Re-run after adding both
- **Gates:**
  - `answer-is-propagated` → **pass** — each file named in `## Consequences` opened and checked
    after writing: `artifacts/refinement-qa.md` carries the stakeholder's words verbatim under
    Round 1 in place of `[unresolved]`, is `status: recorded`, has AC3/AC5 resolved and AC3b
    added; `item.md`'s "Where refinement got to" section now states option A, that no question is
    open, and that the Definition of Ready failure set is R4 and R10. Neither file still says
    Q-001 is open.
  - `answered-from-the-record` → **pass** — the answer is the stakeholder's own reply, quoted
    verbatim with its timestamp in both the question and the Q&A. Nothing was inferred; the two
    downstream statements that go beyond their words (the invariant over `positions()`, and AC3b)
    are each attributed and reasoned in place rather than presented as theirs.
  - `escalation-is-justified` → **skipped** — nothing was escalated. The escalation that produced
    this question was `refine`'s and it has been answered.
  - `workspace-valid` → **pass** — `validate-workspace .` exit 0 (see Commands).
  - `item-resumed-correctly` → **pass** — the suspending row (2026-08-27T00:56:56Z, `draft` →
    `awaiting-answer`, actor `refine`) records `resume-to: draft`; this execution transitions to
    `draft`, not to `ready` and not to `refining`.
  - `a-deferral-is-not-an-answer` → **skipped** — the reply is not a deferral. It selects one of
    the four options by name and gives the reason for selecting it, so there is nothing to park.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-001.md` — `status: open` → `answered`, `answered-at:
    2026-08-27T01:00:12Z`, `answered-by: human`; `## Consequences` written naming both files and
    stating what this answer deliberately does *not* do
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — `status: agenda` → `recorded` (the flip
    the file's own opening paragraph defines as due once the answer is in); Round 1 answer
    written verbatim with what option A fixes and what declining option D rules out; R8 row in
    the entry table updated; AC3 rewritten as the full refusal criterion; AC3b added; AC5's
    person-deletion half stated; the R10 closing paragraph and a new dated section recording that
    the answer closes R6 and R8 and leaves R4 and R10 failing
  - `tracker/items/WI-0004/item.md` — the stale "Where refinement got to" section replaced; `updated` bumped
  - commit of the above under `refs WI-0004`
- **Status:** `awaiting-answer` → `draft`
- **Result:** The stakeholder chose option A — deleting a person named in a recorded expense is
  refused, with the expenses in the way named, and nothing on disk changes. The answer is
  propagated into the Q&A (now `recorded`, with all eight criteria unconditional) and into
  `item.md`, and WI-0004 returns to `draft` for `refine` to install those criteria and judge
  readiness. Definition of Ready R6 and R8 are closed by this; R4 and R10 are not, and are
  `refine`'s to close.

## 2026-08-27T01:07:37Z — refine v0.2.1 — product-analyst

- **Item:** WI-0004
- **Trigger:** `draft` — `next` dispatched this as the highest-ranked runnable item (medium/rank 3,
  created 2026-08-26T23:42:32Z, ahead of BUG-0002 on `created` and BUG-0001 on priority rank).
  This is `refine`'s **second** execution on the item: the first, at 2026-08-27T00:56:56Z, could
  not finish and suspended it to ask the stakeholder Q-001. That question is now answered and
  propagated, so this execution had the one thing it was missing.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the four "a documented command" criteria left deliberately
    unrefined, the `## Out of scope` list, and the `## Notes`
  - `tracker/items/WI-0004/history.md` — read first, per the procedure. This item did **not**
    come back from `verifying` or `in-review`; it reached `draft` twice, once at creation and once
    from `awaiting-answer`. So it is a fresh refinement continuing an interrupted one, not a
    send-back, and there is no specific defect to fix in isolation
  - `tracker/items/WI-0004/journal.md` — the previous `refine` entry and the `answer-questions`
    entry that consumed the answer
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — the agenda, the gap-routing table, D1–D4,
    the eight drafted criteria, and Round 1 now carrying the stakeholder's verbatim answer
  - `tracker/items/WI-0004/questions/Q-001.md` — the answer and its consequences
  - `.claude/agile-skills/spec/dor-dod.md` §1 — the ten Definition of Ready criteria and the
    override rules
  - `tracker/items/WI-0001/item.md` — AC1–AC9, for the criterion style this project already uses
    and for the exact-match naming rule AC7 relies on
  - `expenses/cli.py`, `expenses/store.py` — read to make the criteria decidable against the tool
    that exists: the `<noun> <verb>` argparse surface, `expense_list`'s current line format, the
    `ExpensesError` → stderr → exit `REFUSED` path, and `add_person`'s exact-string comparison
  - `tests/test_cli.py`, `README.md` §`expense list` — to find what D2's number column breaks
- **Decisions:**
  - **Nothing was asked of the stakeholder, and that is a decision with an audit behind it.** The
    `## Who each gap belongs to` table in the Q&A lists every candidate gap and where it was
    routed: one to them (Q-001, now answered), four decided under WI-0001 A1's naming precedent
    and A2's contract for what a command does, three answered from the record or from
    `## Out of scope`, and none to `plan`. Re-opening any of the settled ones would have told them
    their answers were not heard (F-023).
  - **All eight drafted criteria installed, with three changes.** AC3b became AC4 and everything
    after shifted by one. AC3 gained a second case — `person delete Ana`, the payer of the other
    expense — so an implementation that checked only `shared_by`, or only `paid_by`, fails it;
    the drafted version could have been passed by code honouring one role. AC7 grew from two
    refusals to nine, adding `person delete ana` against a group holding `Ana` (this is the first
    command since WI-0001 that looks a name up, and AC1 fixed exact matching), the empty name,
    `expense delete 0`, `-1` and `abc`, and both deletions against an **empty** store where the
    criterion also requires that no data file is created — a refusal that wrote an empty store to
    disk would have passed the draft.
  - **AC8 rewritten from a reading judgement into four present-or-absent checks** — the two
    literal command strings with worked examples, a numbered `expense list` sample, a sentence
    stating the refusal and its remedy, and a sentence stating that numbers renumber. As drafted
    it asked whether the README was adequate, which is the kind of criterion `verify` cannot
    settle without an opinion.
  - **`TWO-EXPENSE STORE` defined once, as a literal command sequence**, and referenced by five
    criteria. Six of the eight criteria depend on a specific starting state; naming it in prose
    each time is how two criteria come to mean slightly different stores.
  - **Three entries added to `## Out of scope`**, each a thing a reader would plausibly assume is
    included and each traceable: the `--and-their-expenses` bulk flag (offered as Q-001 option D
    and declined by the stakeholder — absent by their choice, not by oversight), any confirmation
    prompt (D3), and a stable expense identifier (D2's cost, stated so nobody adds one to be
    helpful).
  - **D2's collateral damage recorded in `## Notes` for `plan`, not fixed here and not asked
    about.** The number column changes `expense list` output WI-0001 delivered. It breaks no
    WI-0001 criterion — AC3 asks for the fields and the recorded order, both untouched by a
    leading number — but it does break one WI-0001 test, which reads the amount as
    `line.split()[1]`, and it makes the README sample wrong. Named so `plan` reconciles it
    deliberately instead of `implement` discovering it as a red test. This is an implementation
    consequence, not a product question.
  - **The stale "Where refinement got to" section removed and replaced** with a shorter "How this
    item got here". Leaving it would have left the item asserting that a question is open and
    that R4 and R10 fail, both of which this execution made untrue.
  - **No override recorded, and none invented.** All ten criteria pass on their own terms.
- **Questions raised:** none. Round 1's single question (`questions/Q-001.md`) was asked by the
  previous execution and is answered; this execution asked nothing and left nothing
  `[unresolved]`. The full exchange and every `[assumed]` decision are in
  `artifacts/refinement-qa.md`, `status: recorded`.
- **Commands:**
  - `validate-workspace .` → exit 0 before and after each edit; four runs, all clean
  - `sed`/`python3` edits to `item.md` and `artifacts/refinement-qa.md` → one of them spliced a
    section against an index that appeared earlier in the file than the anchor it replaced and
    duplicated three `## Notes` subsections; caught by re-reading the whole item, fixed by
    deleting the first copies, verified by counting each heading (1 each) and re-validating
  - `transition WI-0004 --to ready --actor refine --journal-body-file ...` → see Status
- **Gates:**
  - `workspace-valid` → **pass** — `validate-workspace .` exit 0, 7 items and 7 documents, 0
    errors and 0 warnings, re-run after the last edit
  - `definition-of-ready` → **pass**, criterion by criterion. R1 pass [auto]. R2 pass — the story
    names the role ("the person keeping track of the group's costs"), the capability (delete a
    person or an expense recorded by mistake) and the outcome ("so that a typo does not sit in
    every who-owes-whom answer for ever"). R3 pass [auto] — AC1–AC8. **R4 fail on entry → pass**:
    the four "a documented command" criteria named no command; each of AC1–AC8 now names one and
    the observation that settles it — exact stdout for successes, exit code plus unchanged
    `md5sum` for refusals, a byte comparison for persistence, four present-or-absent checks for
    the README. No unmeasurable adjective remains. R5 pass — six `## Out of scope` entries, three
    added here. R6 pass [auto] — Q-001 is `answered`, nothing open. R7 pass [auto] —
    `depends-on: WI-0002`, `done`. R8 pass [auto] — `refinement-qa.md` at `status: recorded`, the
    stakeholder's answer verbatim, every assumption tagged `[assumed]` with the deferral it rests
    on. R9 pass — one command surface, one storage operation, one refusal path; splitting would
    have produced two items both needing Q-001's answer. **R10 fail on entry → pass**: `## Notes`
    now carries the combination map naming which criterion states each pairing and which pairings
    are excluded instead, with nothing left deliberately unconstrained
  - `criteria-are-decidable` → **pass** — each criterion was taken in turn and the settling
    observation stated: AC1/AC4 exact stdout and exact `person list` output; AC2 first-field
    comparison and exact `no expenses`; AC3 exit code, empty stdout, stderr containing the name
    and the count, `md5sum` unchanged; AC5 byte comparison across a fresh process; AC6 three exact
    `settle` outputs; AC7 nine commands each checked for exit code, stderr, empty stdout and an
    unchanged or absent data file; AC8 four literal present-or-absent checks. The exit codes are
    written as "non-zero" rather than `2` deliberately, matching WI-0001's criteria — `REFUSED`
    is an implementation constant and pinning it in a criterion would freeze it by accident
  - `qa-recorded-verbatim` → **pass** — the stakeholder's answer is quoted word for word in Round
    1 of `refinement-qa.md` and again in `item.md`; nothing was paraphrased into confidence.
    D1–D4 are tagged `[assumed]` and say plainly that the stakeholder was **not** asked, and the
    file states exactly what their silence on those does and does not amount to. Nothing is
    `[unresolved]`
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` — `## Acceptance criteria` replaced (four vague → AC1–AC8
    with a shared `TWO-EXPENSE STORE` definition); three `## Out of scope` entries added; `##
    Notes` gained D1–D4, "What D2 costs elsewhere", the R10 combination map and "How this item got
    here", and lost the stale bullet and the stale "Where refinement got to" section
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — the opening paragraph corrected to say
    this second execution closed R4 and R10; AC3b marked as installed as AC4; a closing section
    recording that nothing was asked and why, the three changes made while installing, D2's cost,
    and the per-criterion Definition of Ready verdict
  - commit of the above under `refs WI-0004`
- **Status:** `draft` → `ready`
- **Result:** WI-0004 is Ready, with no override. The stakeholder's Q-001 answer became AC3 and
  AC4; the remaining six criteria pin the successes, persistence, the interaction with `settle`,
  the nine ways a deletion can be refused, and the README. `plan` inherits one flagged
  consequence: D2's number column breaks a WI-0001 test and the README sample, both named in
  `## Notes` so they are reconciled rather than discovered.

## 2026-08-27T01:12:22Z — plan v0.3.0 — architect

- **Item:** WI-0004
- **Trigger:** `ready` — `next` dispatched this as the highest-ranked runnable item (medium/rank 3,
  created 2026-08-26T23:42:32Z, ahead of BUG-0002 on `created` and BUG-0001 on priority rank).
  First planning of this item; `history.md` shows no rejection or send-back, so this is a fresh
  design and not a re-plan.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC8, the six `## Out of scope` entries, D1–D4, the R10
    combination map, and the "What D2 costs elsewhere" note left by `refine` for this execution
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — the four `[assumed]` decisions (the soft
    ground this design either confirms or overturns), the gap-routing table, and Round 1
  - `tracker/items/WI-0004/questions/Q-001.md` — the stakeholder's own words on the refusal
  - `tracker/items/WI-0004/history.md` and `journal.md`
  - `docs/architecture/overview.md` v3 — the one-way layering rule, and its "What is coming"
    paragraph on WI-0004
  - `docs/architecture/adr/` — all five existing ADRs read: ADR-0001 (one JSON file, rewritten
    whole), ADR-0002 (integer minor units), ADR-0003 (remainder to the first-named sharers),
    ADR-0004 (unittest, no lint), ADR-0005 (the settlement rule). None conflicts with this item
  - `tracker/project.yaml` — `commands.test` already set for WI-0001; `lint` and `build` null per
    ADR-0004
  - Source actually read, not assumed: `expenses/cli.py` (the argparse surface, `HANDLERS`, the
    single `ExpensesError` → stderr → `REFUSED` path in `main()`, `expense_list`'s line format),
    `expenses/store.py` (`add_person`/`add_expense`'s check-then-mutate shape, `save()` creating
    the parent directory, `VERSION`, the record fields), `expenses/settle.py` (`positions()`
    keying on `data["people"]` and skipping unknown names), `expenses/money.py`
  - `tests/test_cli.py` and `tests/test_store.py` — for the `AC<n><what>` class convention, the
    `run_in_a_new_process` helper AC5 needs, the README-content test precedent, and the one test
    the number column breaks
  - `README.md` §`expense list` — the sample output AC8 replaces
- **Decisions:**
  - **How a single expense is addressed — decided, `ADR-0006`.** Route: **decided** (preference
    order branch 3 was not reached; no document settled it, and it is not irreversible). Refinement
    had recorded the position-based handle as `[assumed]` with two rejected alternatives and
    explicitly left it open for `plan` to overturn with a recorded reason. Confirmed, and the ADR
    adds what refinement could not weigh: option B (a stored opaque id) is not merely more code, it
    is a stored-format change against a `load()` that refuses any `version` but 1, so it implies a
    version bump and a compatibility path. Recorded with its reversibility in both directions.
  - **Where the people-and-expenses invariant is enforced — decided, `ADR-0007`.** The stakeholder
    settled the behaviour; what layer holds it was still open, and the alternatives are real:
    check on read (locks a person out of the tool that would show them what is wrong), make
    `positions()` refuse (does not prevent the state and contradicts their choice), or both (two
    checks that drift). Chosen: enforce at the two write points in `store.py` and change
    `settle.py` not at all. The ADR states the limit explicitly — the guarantee covers data this
    tool wrote and not a hand-edited or externally-imported file — because WI-0003's importer is
    the case that will test it.
  - **Refusals for `expense delete <NUMBER>` go through `ExpensesError`, not argparse `type=int`.**
    Route: **documented** — it follows from the refusal contract WI-0001's refinement fixed, so no
    ADR. `type=int` would route `abc` through argparse's error path while `0` and `-1` came back
    as ordinary refusals; AC7 requires all seven to behave alike.
  - **The AC3 refusal string is fixed in the plan** as `<name> is named in <n> expense(s); delete
    those first` — the string the stakeholder was shown in the option they chose. Route:
    **assumed**, recorded under `## Assumptions` with its reversal cost (one literal and its
    tests). AC3 requires only the name and the count, so the rest is the plan's, and leaving it to
    the developer would leave `verify` with a judgement instead of a comparison.
  - **`naming_expenses` checks `shares_minor`'s keys as well as `paid_by` and `shared_by`.** Route:
    **assumed**. For a dataset this tool wrote the three agree by construction, so it costs nothing
    and can only refuse more.
  - **No test for AC8.** Route: **assumed**, with the reason recorded: AC8 is a reading check and
    a test would pin wording the criterion deliberately leaves open.
  - **BUG-0002 not absorbed.** This plan adds two more callers of `store.save()`, which is where
    that defect lives; it is left alone and named in `## Out of scope for this item`. Widening the
    plan would make both changes unverifiable against their own criteria.
  - **Nothing asked of the human.** Every decision here is reversible and none turns on intent no
    document records; the one that did was asked before the item was Ready.
- **Questions raised:** none.
- **Commands:**
  - `validate-workspace .` → exit 0, three times (before writing, after the ADRs and plan, after
    the overview update); 7 items and 9 documents at the end
  - `lint-claims --changed-since main` → exit 1 first, two `claim.unsourced` errors in ADR-0006
    ("no lookup structure is needed" about `store.expenses(data)`, and "no worse" about
    `VERSION`); both given resolvable `[src: expenses/store.py]` citations → re-run exit 0, then
    exit 0 again over all three changed documents
  - `python3 -m unittest discover -s tests -t .` → `Ran 86 tests`, `OK` — run to confirm
    `commands.test` is a command that actually works in this project before declaring the gate
- **Gates:**
  - `workspace-valid` → **pass** — `validate-workspace .` exit 0, 0 errors and 0 warnings, on the
    final state
  - `every-criterion-is-addressed` → **pass** — the `## Acceptance criteria mapping` table in
    `plan.md` has one row per criterion, AC1 through AC8, each naming the plan steps that satisfy
    it and the specific test class or reading that demonstrates it. No row says "tests": AC3 and
    AC7 name the byte-comparison of the data file, AC5 names the existing `run_in_a_new_process`
    helper, AC7 names the nine argument vectors and the two empty-store cases, AC8 names the four
    things to read the README for. Every step in `## Steps` maps to at least one AC row except
    steps 7 and 11, which are the regression repair the change forces and the gate run itself
  - `project-commands-resolved` → **pass** — `commands.test` is
    `python3 -m unittest discover -s tests -t .`, set for WI-0001 and **run by this execution**:
    86 tests, OK. `lint` and `build` stay null, with ADR-0004 as the record of why; the matching
    gates are recorded as skipped citing it, not as passes
  - `decisions-recorded` → **pass** — seven choices listed above, each with a route. Two point to
    ADRs written by this execution (ADR-0006, ADR-0007), each with at least two options, their
    costs and their risks, and an explicit reversibility paragraph. Four point to entries under
    `plan.md`'s `## Assumptions`, each stating what reversal would cost. One is documented from
    the existing refusal contract. Nothing is deferred to `implement` as "handle appropriately"
  - `claims-are-sourced` → **pass** — `lint-claims --changed-since main` exit 0 over the three
    changed documents, after fixing the two unsourced absolutes it caught in ADR-0006
  - `plan-is-executable-without-you` (advisory) → **pass, with one reservation recorded.** The
    plan was re-read cold: every step names its file and what is true afterwards, the three new
    function contracts are given as signatures and docstrings with the bodies left to the
    developer, and the three strings that criteria constrain are fixed in the plan rather than
    left to taste. The reservation: step 9 says "a class per acceptance criterion" without
    enumerating the assertions, deliberately — the criteria already state them exactly, and
    restating them in the plan would create a second copy to drift
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/plan.md` — created, all ten required sections
  - `docs/architecture/adr/ADR-0006-an-expense-is-addressed-by-its-position-in-the-listing.md` —
    created, v1, three options
  - `docs/architecture/adr/ADR-0007-referential-consistency-is-enforced-where-data-is-written.md` —
    created, v1, four options
  - `docs/architecture/overview.md` — v3 → **v4**, with a change-log row. "What is coming" now
    records WI-0004's actual shape and the two ways it changes the system rather than adds to it,
    following the precedent WI-0002's plan set of writing the shape before the code exists
  - `tracker/project.yaml` — unchanged; already resolved for WI-0001
  - commit of the above under `refs WI-0004`
- **Status:** `ready` → `planned`
- **Result:** WI-0004 is planned as eleven steps over `expenses/store.py`, `expenses/cli.py`, the
  two test modules and `README.md`, with no new module and no change to the stored format. Two
  ADRs record the decisions that outlive the item: ADR-0006 fixes how an expense is addressed and
  what that costs, ADR-0007 names the people-and-expenses invariant, puts it at the write points,
  and states where it stops — the fact WI-0003's importer will need. `implement` inherits one
  regression it must repair rather than discover (step 7) and one defect it must leave alone
  (BUG-0002).

## 2026-08-27T01:14:36Z — implement v0.2.1 — developer

- **Item:** WI-0004
- **Trigger:** status `planned`, dispatched by `next` as the highest-ranked runnable item (priority medium, created 2026-08-26T23:42:32Z, ahead of BUG-0002 on `created` and of BUG-0001 on priority-rank)
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC8, the out-of-scope list, and D1–D4
  - `tracker/items/WI-0004/artifacts/plan.md` — the eleven steps, the fixed refusal string, and the AC mapping
  - `tracker/items/WI-0004/history.md` — five rows; the last is `ready → planned`, so this is a fresh start, not a resumption
  - `tracker/items/WI-0004/questions/Q-001.md` — `status: answered`, propagated into `item.md` (AC3, AC4) before this run
  - `tracker/project.yaml` — `commands.test`, `commands.lint: null`, branch prefix `wi/`, commit subject convention
  - `docs/architecture/adr/ADR-0006-*.md` and `ADR-0007-*.md` — the position handle and where the people/expenses invariant lives
  - `expenses/store.py`, `expenses/cli.py`, `expenses/settle.py`, `expenses/money.py` — the code the plan changes and the code it must leave alone
  - `tests/test_cli.py`, `tests/test_store.py` — the existing suites, including the WI-0001 test step 7 must repair
  - `README.md` — the sample output AC8 requires replacing
- **Decisions:**
  - none yet — this entry opens the execution. Every decision this run takes will be in the closing entry.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0004 main` → 0 (branch created from the trunk; no branch existed before)
- **Gates:**
  - `tests-pass` → **not yet run** (no change has been made)
  - `lint-clean` → **not yet run**
  - `workspace-valid` → **not yet run**
  - `every-criterion-has-a-test` → **not yet run**
  - `commits-reference-the-item` → **not yet run** (no commits on the branch)
  - `claims-are-sourced` → **not yet run**
  - `no-unplanned-scope` (advisory) → **not yet run**
- **Artifacts:**
  - branch `wi/WI-0004`, at `main` with no commits of its own yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0004 has started on a fresh branch. The plan is executable as written: nothing in it conflicts with the code as it stands, and the WI-0001 test and README that D2's number column disturbs are steps 7 and 10 rather than surprises.

## 2026-08-27T01:19:22Z — implement v0.2.1 — developer

- **Item:** WI-0004
- **Trigger:** status `in-progress` — this execution's own opening entry, continued to completion in the same session
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC8, `## Out of scope`, D1–D4
  - `tracker/items/WI-0004/artifacts/plan.md` — the eleven steps, the fixed refusal string, the assumptions
  - `tracker/items/WI-0004/history.md`, `tracker/items/WI-0004/questions/Q-001.md`
  - `tracker/project.yaml`; `docs/architecture/adr/ADR-0006-*.md`; `docs/architecture/adr/ADR-0007-*.md`
  - `expenses/store.py`, `expenses/cli.py`, `expenses/settle.py`, `expenses/money.py`
  - `tests/test_cli.py`, `tests/test_store.py`, `README.md`
- **Decisions:**
  - **A test class was added for AC8**, against the plan's fourth assumption. It pins only what AC8 itself fixes — the two literal command strings, the two output lines AC1 and AC2 already fix exactly, and AC8(b)'s numbered sample — and asserts nothing about the prose of AC8(c) or AC8(d), which is the wording the assumption wanted left open. The plan priced this reversal at "a new test class and nothing else". Reason: `every-criterion-has-a-test` is a hard gate, and leaving AC8 with no mechanical check at all made the gate rest on a reading that `verify` would have to repeat from scratch.
  - **An empty name's refusal is quoted** — `'' is not in the group` — rather than interpolated bare into `add_expense`'s message shape, which would have produced a message beginning with a space and naming nothing. One branch, one `%r`. AC7 constrains only that a message is written.
  - **`delete_expense`'s out-of-range message is `there is no expense <n>`.** The plan required a message naming the number and did not fix the string.
  - **AC7's loop covers the seven vectors the criterion enumerates**, not the "nine" the plan's mapping table names; the criterion's own text lists seven, plus the two empty-store cases the plan counts in the same row. Recorded as a deviation rather than silently reconciled.
  - **Decided *not* to make:** nothing. No decision arose that the plan does not make and that is not the developer's. In particular BUG-0002 was left alone even though this item adds two more callers of `store.save()`, and `docs/architecture/overview.md` was left alone because the plan states the layering is unchanged.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0004 main` → 0
  - `python3 -m unittest discover -s tests -t .` → 0, after each step; final run on the branch head `Ran 120 tests … OK`
  - `python3 -m expenses …` by hand against `EXPENSES_STORE=/tmp/wi4store.json`, to see all seven AC7 refusals and the numbered listing → each refusal exit 2 with one line on stderr, including `expense delete -1` → `expense '-1' is not a positive whole number`
  - `git commit` ×2 → 0 (`46dead0`, `ff28637`)
  - `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0
  - `.claude/agile-skills/scripts/validate-workspace .` → 0
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 120 tests`, `OK`, run on the branch head after the last change)
  - `lint-clean` → **skipped** — `commands.lint` is `null` in `tracker/project.yaml`; ADR-0004 records that this project installs nothing and the standard library ships no linter. This gate checked nothing.
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0; 7 items, 9 documents, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** — AC1 `WI0004AC1DeletingAPersonNobodysExpensesName`; AC2 `WI0004AC2DeletingAnExpenseAndTheRenumberingThatFollows`; AC3 `WI0004AC3DeletingAPersonNamedInAnExpenseIsRefused`; AC4 `WI0004AC4TheRefusalIsAboutTheExpensesNotThePerson`; AC5 `WI0004AC5DeletionsSurviveTheProcessExiting`; AC6 `WI0004AC6TheSettlementFollowsTheDeletion`; AC7 `WI0004AC7DeletingSomethingThatIsNotThereIsRefused`; AC8 `WI0004AC8TheReadmeDocumentsBothCommands` for its (a) and (b), and a reading of `README.md` for its (c) and (d). Store-level cover in `tests/test_store.py`. Full mapping in `artifacts/impl-report.md`.
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0: `all 2 commit(s) on main..wi/WI-0004 name WI-0004`)
  - `no-unplanned-scope` (advisory) → **pass** — six files plus the tracker's own record; each traces to a plan step: `README.md` (10), `expenses/cli.py` (4–6), `expenses/store.py` (1–3), `tests/test_cli.py` (7, 9), `tests/test_store.py` (8)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0; it reports no documents changed, because this item touched nothing under `docs/`. `README.md`'s two new `[src: …]` markers were checked by hand against the ADR filenames on disk)
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/impl-report.md` — created
  - `expenses/store.py`, `expenses/cli.py`, `tests/test_store.py`, `tests/test_cli.py`, `README.md` — changed
  - branch `wi/WI-0004`, commits `main..wi/WI-0004` = `46dead0`, `ff28637`, plus this record's own tracker commit
- **Status:** `in-progress` → `verifying`
- **Result:** `person delete` and `expense delete` are implemented as planned, with `expense list` numbering its lines so the second command has something to name. All hard gates pass on the branch head and `lint-clean` is skipped for the reason ADR-0004 records. Three small deviations and one against a plan assumption are in the implementation report; BUG-0002 and the prose halves of AC8 are named there as handovers rather than left for verification to discover.

## 2026-08-27T01:23:31Z — verify v0.1.3 — qa-engineer

- **Item:** WI-0004
- **Trigger:** status `verifying`, dispatched by `next` as the highest-ranked runnable item (medium priority, created 2026-08-26T23:42:32Z, ahead of BUG-0002 on `created` and BUG-0001 on priority-rank)
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC8, read **first** and turned into commands before the implementation was looked at
  - `tracker/items/WI-0004/history.md`
  - `tracker/items/WI-0004/artifacts/plan.md` — the eleven steps and the four assumptions, for the diff read
  - `tracker/items/WI-0004/artifacts/impl-report.md` — read **after** the criteria were checked, and checked rather than trusted
  - `tracker/project.yaml` — `commands.test`, `commands.lint: null`
  - the code on branch `wi/WI-0004` at `f4e8319c2e58bf6daae6e41264ddc1f0c0525f85`: `expenses/store.py`, `expenses/cli.py`, `README.md`, `tests/test_cli.py`, `tests/test_store.py`
- **Decisions:**
  - **AC5 was checked in a way the criterion forces and the obvious method would not have.** Every command in a shell is already a fresh process, so comparing two shell runs proves nothing about persistence. The deletion and the listing were run in **one** python process via `expenses.cli.main`, that listing captured, and a fresh `python3 -m expenses` listing compared to it with `cmp`. Both pairs byte-identical.
  - **Probe 3 of the sensitivity check did not fail, and that is recorded as correct rather than papered over.** Replacing `cli.parse_position`'s refusal with `int()` and a `0` fallback left every AC7 observation true, because the resulting position is one `store.delete_expense` refuses anyway. The probe moved the behaviour rather than removing it; probe 5 removes it, and the AC7 tests fail there. Recorded in the report with the reasoning, because a probe that passes looks like an insensitive test unless the reason is written down.
  - **No criterion was judged `ambiguous`.** Each of AC1–AC8 named a command and an observation precise enough to decide without interpretation — including the byte-level ones, which were settled with `od -c` and `cmp` rather than by eye.
  - **No send-back and no bug item.** Nothing failed. The one thing that could have been a defect against another item — `expense list`'s new leading column changing output WI-0001 delivered — was checked against WI-0001 AC3 directly, which asks for amount, payer, sharers, date and description in recorded order. All five are still there in that order; the position is prepended, not substituted. Not a regression, so nothing to file.
  - **Two behaviours exist that no criterion names**, and both were traced to the plan rather than treated as unrequested scope: `naming_expenses` also checks `shares_minor`'s keys (plan assumption 2 — it can only refuse more), and `parse_position` strips whitespace, as `parse_date` and `add_person` already do.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → 0 (`f4e8319c2e58bf6daae6e41264ddc1f0c0525f85`)
  - `python3 -m unittest discover -s tests -t .` → 0 (`Ran 120 tests in 1.206s`, `OK`)
  - AC1: `person add Ana`, `person add Ben`, `person delete Ben` → 0, `person list` → 0; both stdouts dumped with `od -c`
  - AC2: the TWO-EXPENSE STORE built from the item's four commands, then `expense list` → 0, `awk '{print $1}'` → `1`,`2`, `expense delete 2` → 0, `expense list` → 0 (1 line), `expense delete 1` → 0, `expense list` → 0 (`no expenses`)
  - AC3: `md5sum` / `person delete Ben` → 2 / `md5sum`; same for `Ana`; `person list` → 0
  - AC4: `expense delete 1` → 0 twice, `expense list` → 0, `person delete Ben` → 0, `person list` → 0
  - AC5: a python heredoc calling `expenses.cli.main` for the deletion and the listing in one process, then `python3 -m expenses <listing>` and `cmp` → 0, twice
  - AC6: `settle` → 0, `expense delete 1` → 0, `settle` → 0; then on a rebuilt store `settle` → 0, `person delete Ben` → 2, `settle` → 0, `cmp` → 0
  - AC7: seven argument vectors against the two-expense store, each with `md5sum` before and after → all exit 2; two vectors against a missing file → both exit 2, `[ -e $S ]` false
  - AC8: `grep -n "person delete\|expense delete" README.md` → 0; `sed -n '/\$ python3 -m expenses expense list/,/^```$/p' README.md` → 0; read of lines 50–70 and 111–126
  - sensitivity probes 1–6, each followed by `git checkout -- <path>` and `git status --short` → clean
  - `git diff main..HEAD -- expenses/ README.md` → 0
  - `python3 -m expenses person delete --help` → 0; `expense delete --help` → 0; `python3 -m expenses expense` → 2
  - `.claude/agile-skills/scripts/validate-workspace .` → 0
- **Gates:**
  - `tests-pass` → **pass** — `python3 -m unittest discover -s tests -t .` run by this skill on `f4e8319`: exit 0, `Ran 120 tests`, `OK`
  - `lint-clean` → **skipped** — `commands.lint` is `null` in `tracker/project.yaml`; ADR-0004 records why this project has no linter. The gate checked nothing, and `## Not verified, and why` says what that leaves unchecked
  - `workspace-valid` → **pass** — `validate-workspace .` exit 0, 7 items, 9 documents, 0 errors, 0 warnings
  - `every-criterion-independently-checked` → **pass** — the report's Criteria table gives, for each of AC1–AC8, the command this skill ran and its actual output. No row's evidence is `impl-report.md`
  - `negative-cases-exercised` → **pass** — AC3's two refusals, AC7's seven vectors and two empty-store cases, AC6's refused deletion and AC2's last-expense boundary were all triggered; eleven listed in the report
  - `tests-would-fail-without-the-change` (advisory) → **pass** — six probes, five failing as expected and one recorded as a behaviour-preserving move rather than a removal, with probe 5 covering the same criterion. Tree restored and confirmed clean after each
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/verify-report.md` — created, with `Verified-commit: f4e8319c2e58bf6daae6e41264ddc1f0c0525f85`
  - `tracker/items/WI-0004/item.md` — AC1–AC8 ticked, each against a command run in this execution
  - bug items filed: none
- **Status:** `verifying` → `in-review`
- **Result:** All eight criteria pass on `f4e8319`, each decided by a command run here rather than by the implementation report. The refusal that protects `settle` from computing over a deleted person works in both directions — the deletion is refused, and the settlement is byte-identical across the attempt. No defect was found and nothing was sent back; four gaps are declared in `## Not verified, and why`, of which the substantive one is that `lint-clean` checked nothing because this project has no linter.

## 2026-08-27T01:27:21Z — review-close v0.4.0 — reviewer

- **Item:** WI-0004
- **Trigger:** status `in-review`, dispatched by `next` as the highest-ranked runnable item (medium priority, created 2026-08-26T23:42:32Z, ahead of BUG-0002 on `created` and BUG-0001 on priority-rank)
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `history.md` (all eight rows), `journal.md` (read in full, eight entries), `questions/Q-001.md`
  - `tracker/items/WI-0004/artifacts/plan.md`, `impl-report.md`, `verify-report.md`
  - the diff `main..wi/WI-0004`, hunk by hunk, split across `-- expenses/store.py`, `-- expenses/cli.py`, `-- README.md` and `-- tests/`
  - `docs/architecture/overview.md` v4 (in full), `docs/product/vision.md`, `docs/architecture/adr/ADR-0006-an-expense-is-addressed-by-its-position-in-the-listing.md`, `docs/architecture/adr/ADR-0007-referential-consistency-is-enforced-where-data-is-written.md`
  - `tracker/project.yaml`, `.claude/agile-skills/spec/dor-dod.md` §3
- **Decisions:**
  - **Rejected, back to `in-progress`, on one finding (F1).** `docs/architecture/overview.md` is still at version 4, and version 4 describes this item's work under `## What is coming`. It is delivered. That is **D7**. Worse, the sentence doing the describing says `store.py` gains "two new functions"; it gains three — `naming_expenses`, `delete_person`, `delete_expense`, confirmed with `grep -n "^def " expenses/store.py` on the branch head. That is **D12**, and it is the exact failure mode D12 was written for: the claim was re-quoted from the plan's `## Approach` summary (which also says two) rather than checked against the plan's own steps or the code.
  - **Why a send-back and not an accepted gap.** `impl-report.md` declared this under `## What I did not do`, reasoning that the plan lists no step for the overview because the layering is unchanged. The layering being unchanged is true and is not what D7 asks. D7 asks whether the change invalidated a document, and it did — in tense, and in a fact. The remedy has in-document precedent: `overview.md`'s own change-log row 3 records `implement` moving WI-0002's `settle` out of `## What is coming` into the body on delivery. Accepting it as a recorded gap would leave a false sentence about named code in the architecture overview, which is what D12 exists to stop.
  - **Not sent back to `verifying`.** `check-verify-freshness` reports the verification still covers the code: the branch moved from `f4e8319` to `e50dc4f`, but only five files under `tracker/` changed. The verification is current and the criteria are properly evidenced; the defect is in the docs, which is implementation work.
  - **F2 recorded and explicitly not to be acted on.** `naming_expenses` returns `(position, expense)` pairs and no caller reads the positions. The shape is the architect's, fixed in `plan.md`, and is what a future message naming *which* expenses would need. Narrowing it would be scope no criterion covers, so the review says so rather than leaving the next developer to guess.
  - **F3 — the four deviations in `impl-report.md` were checked rather than taken on trust**, including the one against a plan assumption (a test class for AC8). It pins only AC8(a)'s literals, AC1's and AC2's exact output lines and AC8(b)'s numbered sample, leaving the prose of (c) and (d) to a reader — so the assumption's purpose survives. All four are sound; none is a finding.
  - **F4 — no ADR is contradicted and there is no unrequested scope.** Every hunk maps to a plan step. The two behaviours no criterion names (`naming_expenses` also checking `shares_minor` keys; `parse_position` stripping whitespace) are both in the plan.
  - **The trial merge was run and discarded before deciding**, so that the send-back could say F1 is the *only* thing in the way. It merged with no conflict and the suite passed on the merge result. Nothing was published.
  - **The engagement was not ended.** `scripts/engagement-state EP-001` → `active — still in flight: BUG-0001, BUG-0002, WI-0004`. Not at rest, so no sign-off question was filed and none was due.
  - **Two gaps that would have needed writing into `item.md`'s `## Notes` at a close** — that `lint-clean` checks nothing on this project, and that AC8(c) and AC8(d) are verified by reading only — are carried in `review.md`'s `## Accepted gaps` so the round trip does not lose them.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/check-verify-freshness WI-0004 wi/WI-0004` → 0 (`verified at f4e8319c; … only the record changed (5 file(s) under tracker/ or docs/)`)
  - `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0 (`all 4 commit(s) on main..wi/WI-0004 name WI-0004`)
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0 (`checked no documents changed since main`)
  - `.claude/agile-skills/scripts/check-epic-signoff WI-0004` → 0 (`WI-0004 is a 'work-item', not an epic … PASS`)
  - `.claude/agile-skills/scripts/engagement-state EP-001` → 0 (`active`)
  - `.claude/agile-skills/scripts/validate-workspace .` → 0
  - `git diff main..wi/WI-0004 -- expenses/store.py` / `-- expenses/cli.py` / `-- README.md`; `git diff main..wi/WI-0004 -- expenses/settle.py` → empty
  - `grep -n "^def " expenses/store.py` → `naming_expenses` 126, `delete_person` 145, `delete_expense` 162
  - `git worktree add -q /tmp/trial4 main`; `git -C /tmp/trial4 merge --no-edit wi/WI-0004` → 0, no conflict, 11 files changed; `python3 -m unittest discover -s /tmp/trial4/tests -t /tmp/trial4` → 0 (`Ran 120 tests`, `OK`); `git worktree remove --force /tmp/trial4` → 0
- **Gates:**
  - `definition-of-done` → **fail** — walked D1–D12 individually, table in `artifacts/review.md`. D1–D6, D8, D10, D11 pass; **D7 fails** (`docs/architecture/overview.md` still at v4, describing delivered work as coming) and **D12 fails** ("two new functions in `store.py`" — there are three). D9 not reached: the item is rejected and the branch is left unmerged
  - `verification-postdates-the-code` → **pass** — `check-verify-freshness` exit 0; compared by the script, not judged by how the last commits looked
  - `commits-reference-the-item` → **pass** — `check-commit-refs` exit 0, 4 of 4 commits
  - `tests-pass-on-the-merge-result` → **pass** — run on the trial merge of `wi/WI-0004` into a throwaway worktree of `main`: `Ran 120 tests in 1.232s`, `OK`. The trial was then discarded and the branch was **not** merged, because the item is rejected
  - `workspace-valid` → **pass** — `validate-workspace .` exit 0, 7 items, 9 documents, 0 errors, 0 warnings
  - `record-is-reconstructible` → **pass** — from the tracker, `docs/` and `git log --grep WI-0004` alone: *what was built and why* — two delete commands and a numbered listing, because the stakeholder asked to be able to remove a mistake (`WI-0001/Q-003`, quoted in `item.md`); *which skill decided what* — `refine` the criteria, `plan` ADR-0006 and ADR-0007 and the eleven steps, `implement` the four declared deviations, `verify` the eight verdicts; *what questions arose and how they were resolved* — Q-001 to the stakeholder on what deleting a person does to their expenses, answered option A, propagated into `refinement-qa.md` and `item.md` as AC3 and AC4; *what verification found* — all eight criteria passing with commands and output, no defects, four declared gaps. The one thing the record got wrong is F1, which is why this gate passing and `definition-of-done` failing are consistent: the record is complete, and one sentence in it is untrue
  - `claims-are-sourced` → **pass** — `lint-claims --changed-since main` exit 0. It reports no documents changed since `main`, which is itself part of F1: this item changed nothing under `docs/`, and it should have. The gate proves citations *resolve*; whether they *support* the sentence is the D12 read, and that is the half that failed
  - `epic-sign-off` → **pass (not applicable)** — `check-epic-signoff WI-0004` exit 0: the termination gate applies to an epic's ending, and this is a work item. `engagement-state EP-001` says `active`, so no sign-off was due
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/review.md` — created, with the D1–D12 table, the seven-row D12 claim audit, and five findings
  - merge commit: **none** — the branch is deliberately left unmerged at `e50dc4f`
  - bug items filed: none — F1 is this item's own delivery, so it is a send-back, not a bug
  - sign-off question: none — the engagement is not at rest
- **Status:** `in-review` → `in-progress`
- **Result:** Rejected on one finding. The code is sound — eight criteria evidenced, a diff that maps hunk-for-hunk to the plan, no ADR contradicted, a clean trial merge with 120 tests passing on the merge result — but `docs/architecture/overview.md` still calls this item's delivered work "coming" and, in the same sentence, says `store.py` gains two new functions when it gains three. That is D7 and D12. Fixing it is one document: version 5, a change-log row, the deletion paragraph moved into the body's `store.py` and `cli.py` pieces with ADR-0007's invariant stated there, and the count corrected or dropped.

## 2026-08-27T01:28:17Z — review-close v0.4.0 — reviewer

- **Item:** WI-0004
- **Trigger:** a correction to the entry immediately above, written by the same `review-close` execution. No status change; the item stays at `in-progress` where that entry left it.
- **Inputs read:**
  - the previous entry on this journal, and `tracker/items/WI-0004/artifacts/review.md` §Findings F5, both of which contained the wrong claim
  - `git reflog show main`, `git log --oneline -3 main`, `git remote -v`
- **Decisions:**
  - **What was wrong.** The entry above, and `review.md`'s finding F5, both said the trial merge was discarded and "never published". It was not. `git worktree add -q /tmp/trial4 main` checks out the **real** `main` branch into a second working directory — it does not make a throwaway copy of it, which is what this skill's step 8 asks for. `git -C /tmp/trial4 merge --no-edit wi/WI-0004` therefore fast-forwarded the actual `main` ref from `441a9b0` to `e50dc4f`, and `git worktree remove --force /tmp/trial4` removed the directory without moving the ref back.
  - **How it was caught.** Not by re-reading; by a gate. `check-commit-refs` in the gate run of the rejecting transition reported `wi/WI-0004 is already merged into main, so main..wi/WI-0004 is empty and this gate has nothing left to inspect` — which is exactly the failure that script's message warns about, and it fired within a minute of the mistake.
  - **What was done.** `git branch -f main 441a9b0`, taking the target from `git reflog show main` where `main@{1}` is the pre-merge commit. `main` is not checked out in this working directory — `wi/WI-0004` is — so nothing in the tree moved. `check-commit-refs WI-0004 wi/WI-0004` then returned exit 0, `all 4 commit(s) on main..wi/WI-0004 name WI-0004`, and `git log --oneline main..wi/WI-0004` still lists all four commits.
  - **What was lost: nothing.** The merge was a fast-forward, so no merge commit was created and none was orphaned; the branch is untouched; and `git remote -v` is empty, so nothing left this repository. The premature merge existed for about two minutes inside one local repo.
  - **What stands from the previous entry.** Everything except the isolation claim. The merge result really was clean — no conflict, 11 files changed — and `python3 -m unittest discover -s /tmp/trial4/tests -t /tmp/trial4` really did print `Ran 120 tests in 1.232s`, `OK`. The rejection of WI-0004 on D7 and D12 is unaffected: it rests on `docs/architecture/overview.md`, not on the merge.
  - **The rule this establishes for this project**, recorded because the next execution will reach for the same command: a trial merge must use a **detached** checkout or a copied repository. `git worktree add <path> <trunk>` moves the trunk branch itself and is not a throwaway copy of it.
- **Questions raised:** none
- **Commands:**
  - `git log --oneline -3 main` → 0 (showed `main` at `e50dc4f` — the branch head, i.e. merged)
  - `git reflog show main` → 0 (`e50dc4f main@{0}: merge wi/WI-0004: Fast-forward`; `441a9b0 main@{1}: commit: …`)
  - `git remote -v` → 0, empty
  - `git branch -f main 441a9b0` → 0
  - `git log --oneline -1 main` → 0 (`441a9b0`)
  - `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0 (`all 4 commit(s) on main..wi/WI-0004 name WI-0004`)
  - `git log --oneline main..wi/WI-0004` → 0, four commits
- **Gates:**
  - `commits-reference-the-item` → **pass, on re-run after the repair** — this is the gate that failed in the entry above (`wi/WI-0004 is already merged into main`) and the reason that failure was not the item's fault. It now reports `all 4 commit(s) on main..wi/WI-0004 name WI-0004`
  - `workspace-valid` → **pass** — `validate-workspace .` exit 0
  - every other gate → **unchanged from the entry above**; this correction touched the git ref and two record files, not the item's code, its criteria, or its verification
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/review.md` — finding F5 corrected in place, with the correction stated in the file rather than the false sentence silently removed
  - `main` — rewound to `441a9b0`; `wi/WI-0004` unchanged at `e50dc4f`
- **Status:** `in-progress` → `in-progress`
- **Result:** A correction, not a new judgement. This execution's trial merge accidentally fast-forwarded the real `main`, because `git worktree add <path> main` checks out that branch rather than copying it. `check-commit-refs` caught it inside the same minute, `main` was rewound to `441a9b0`, and the gate now passes. Nothing was lost and nothing left the repository. The rejection of WI-0004 on D7 and D12 stands unchanged, and `review.md` now says what actually happened.

## 2026-08-27T01:32:04Z — implement v0.2.1 — developer

- **Item:** WI-0004
- **Trigger:** status `in-progress`, dispatched by `next`. This is a **resumption after a send-back**, not a fresh start: `review-close` rejected the item at 2026-08-27T01:27:21Z on Definition of Done D7 and D12, and the branch already carries the whole implementation.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the eight acceptance criteria, all ticked; `## Out of scope`; D1–D4
  - `tracker/items/WI-0004/history.md` — nine rows; the last is the send-back `in-review → in-progress`
  - `tracker/items/WI-0004/artifacts/review.md` — **read first**, per this skill's step 1, because the last history row is a send-back. Finding F1 is the whole of it
  - `tracker/items/WI-0004/journal.md` — the two `review-close` entries, including the correction about the trial merge that briefly fast-forwarded `main`
  - `tracker/items/WI-0004/artifacts/plan.md` — the eleven steps, and the `## Approach` summary whose "two new functions" phrasing is the source of the false claim
  - `tracker/items/WI-0004/questions/Q-001.md` — `status: answered`, nothing new since the last entry
  - `docs/architecture/overview.md` (v4) — the document under repair
  - `docs/architecture/adr/ADR-0007-…md` — `## Decision`, for the invariant's exact wording
  - `tracker/project.yaml` — `commands.test`, `commands.lint` (null), the branch prefix and commit convention
  - `expenses/store.py` — `grep -n "^def "`, to count the module-level functions the document makes a claim about
- **Decisions:**
  - **Reconciliation before building.** The branch `wi/WI-0004` exists at `af331b8` with five commits, four of them this item's (`main..wi/WI-0004`); `git status` is clean. Plan steps 1–11 are **all already done** on it — `store.py` steps 1–3, `cli.py` steps 4–6, the WI-0001 test repair step 7, the two test suites steps 8–9, the README step 10, and the gate run step 11 — and `verify` passed all eight criteria against `f4e8319`. Nothing on the plan is redone.
  - **The work of this execution is finding F1 and nothing else.** `docs/architecture/overview.md` at version 5: the deletion paragraph moved out of `## What is coming` into the body, the function count corrected, ADR-0007's invariant stated as a property of the delivered code, a change-log row. F2 (`naming_expenses` returning positions no caller reads) is explicitly marked "do not act on"; F3–F5 require no action. Touching anything else would be the "fixing things you noticed on the way" failure this skill names.
  - **Not re-litigating the plan.** The plan has no step for `docs/architecture/overview.md`; that omission is what D7 caught. Writing the document now is the send-back's instruction, not a change to the design — no ADR moves, no criterion changes, no code changes.
  - **No opening transition.** The item is already at `in-progress`, put there by the send-back, so there is no status move to make and this entry accompanies none. This entry exists so that an interruption before the closing one still shows what was read and what was found already done.
- **Questions raised:** none
- **Commands:**
  - `git log --oneline main..wi/WI-0004` → 0 (four commits, all naming WI-0004)
  - `git status --short` → 0, empty
  - `git diff --stat main..wi/WI-0004` → 0 (12 files, 1125 insertions)
  - `grep -n "^def " expenses/store.py` → 0 (eleven module-level functions; `naming_expenses`, `delete_person`, `delete_expense` are the three this item added)
- **Gates:**
  - `tests-pass` → **not yet run** — will be run on the branch head after the last change
  - `lint-clean` → **not yet run** (and will be `skipped`: `commands.lint` is `null` per ADR-0004)
  - `workspace-valid` → **not yet run**
  - `every-criterion-has-a-test` → **not yet run**
  - `commits-reference-the-item` → **not yet run**
  - `claims-are-sourced` → **not yet run**
  - `no-unplanned-scope` (advisory) → **not yet run**
- **Artifacts:** none yet — the branch `wi/WI-0004` already exists at `af331b8` and was not re-created
- **Status:** `in-progress` → `in-progress`
- **Result:** Implementation resumed on a send-back. The plan is fully executed on the branch and the code is untouched; the outstanding work is finding F1 alone — `docs/architecture/overview.md` version 5, moving this item's delivered work out of "What is coming" and correcting the claim that `store.py` gains two new functions when it gains three.

## 2026-08-27T01:35:10Z — implement v0.2.1 — developer

- **Item:** WI-0004
- **Trigger:** status `in-progress` after `review-close` rejected the item on Definition of Done D7 and D12; dispatched by `next`. Second execution of `implement` on this item.
- **Inputs read:**
  - `tracker/items/WI-0004/artifacts/review.md` — finding F1, which is the whole of the send-back, and F2–F5, which the review marks as requiring no action
  - `tracker/items/WI-0004/item.md`, `history.md`, `journal.md`, `questions/Q-001.md`, `artifacts/plan.md` — listed in full in this execution's opening entry
  - `docs/architecture/overview.md` (v4) and `docs/architecture/adr/ADR-0007-…md` `## Decision`
  - `expenses/store.py`, `expenses/cli.py` — opened to check every claim before writing it, which is the step whose absence caused the D12 failure
  - `tracker/project.yaml`
- **Decisions:**
  - **The fix is one document and nothing else.** `docs/architecture/overview.md` at version 5: the deletion paragraph moved out of `## What is coming` into the `expenses/store.py` and `expenses/cli.py` pieces, the function count corrected from two to three, ADR-0007's invariant stated as a property of the delivered code with its two write points, `## What is coming` reduced to WI-0003, a change-log row, and the header's `version`/`updated`/`updated-by`/`updated-for` fields. `git diff af331b8..HEAD --stat` is that one file.
  - **Every claim was checked against the code, not against the plan.** The false claim came from re-quoting the plan's `## Approach` summary; re-quoting it again would have reproduced the defect. Eight claims, each opened: `grep -n "^def " expenses/store.py` for the count of three; `store.py:126-142` for `naming_expenses`' three routes; `store.py:151-155` for the refusal that names the count; the single additive hunk `@@ -121,3 +121,47 @@` for "nothing was added to `load`"; `store.py:15` for `VERSION = 1`; `cli.py:32,34,35` and `:42,53,54` for three actions under each noun; `cli.py:139-147` for the position column; `store.py:162-166` for the renumbering. The table is in `impl-report.md` `## Round 2`.
  - **F2 was left alone, on the review's explicit instruction.** `naming_expenses` still returns `(position, expense)` pairs that only `len()` reads. Narrowing it would be scope no criterion covers, and the review says so in as many words.
  - **The stale bullet in round 1's `## What I did not do` was corrected in place rather than deleted.** It said `docs/architecture/overview.md` "was not updated" and gave a reason; that bullet was the defect declaring itself, and it also contains the same miscount ("the two new store functions"). Struck through, with the correction stated beside it, because a report that quietly loses the sentence loses the evidence of how the miscount propagated.
  - **Declaring an omission does not satisfy a Definition of Done criterion.** Round 1 named this document under `## What I did not do` and moved on. That is the general lesson worth carrying: `## What I did not do` is a handover for things nothing requires, not an exemption from D7.
  - **Not re-litigating the plan.** The plan contains no step for this document — that omission is what D7 caught — but no ADR was added or amended, no acceptance criterion touched, and no code changed. The deviation is recorded in `impl-report.md` rather than resolved by editing the plan.
- **Questions raised:** none. Nothing in F1 required a decision this skill is not entitled to make: the review specified the four changes concretely and every fact they assert is checkable in the code.
- **Commands:**
  - `git log --oneline main..wi/WI-0004` → 0; `git status --short` → 0, clean; `git diff --stat main..wi/WI-0004` → 0 (reconciliation)
  - `grep -n "^def " expenses/store.py` → 0 (eleven functions; three added by this item)
  - `git diff main..wi/WI-0004 -- expenses/store.py | grep "^-" | grep -v "^---" | wc -l` → `0` (the store.py change is purely additive, so `load` is untouched)
  - `git commit` → 0 → `e2a0b3d docs: architecture overview v5 — deletion is delivered, and store.py gained three functions (refs WI-0004)`
  - `python3 -m unittest discover -s tests -t .` → **0**, `Ran 120 tests in 1.204s`, `OK`, on `e2a0b3d`
  - `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0, `all 6 commit(s) on main..wi/WI-0004 name WI-0004`
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0, `checked 1 document(s)`, `0 errors, 0 warnings`
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, `7 item(s), 9 document(s)`, `0 errors, 0 warnings`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 120 tests`, `OK`, run on the branch head `e2a0b3d` after the last change, not before it)
  - `lint-clean` → **skipped** — `commands.lint` is `null` in `tracker/project.yaml`; ADR-0004 records that this project installs nothing and the standard library ships no linter. This gate checked nothing; it is not a pass
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors, 0 warnings)
  - `every-criterion-has-a-test` → **pass** — `impl-report.md`'s round-1 table names a test function for AC1–AC7 and, for AC8, both the reading and `WI0004AC8TheReadmeDocumentsBothCommands`. Round 2 added no criterion, removed none, and changed no test: the suite is the same 120 tests
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0004 wi/WI-0004` exit 0, all 6 commits)
  - `no-unplanned-scope` (advisory) → **pass** — the round-2 diff is `docs/architecture/overview.md` alone. It traces to Definition of Done D7 and review finding F1 rather than to a numbered plan step, which is declared as this round's one deviation
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0). Unlike round 1, where the script reported no changed documents, this round is the first change this item made under `docs/`, so the gate had something to check
- **Artifacts:**
  - `docs/architecture/overview.md` — version 5
  - `tracker/items/WI-0004/artifacts/impl-report.md` — a `## Round 2` section with the claim-audit table, the deviation, the re-run gates and what was left undone; round 1's stale bullet struck and corrected in place
  - commits: `e2a0b3d` (this round); branch `wi/WI-0004` now `main..wi/WI-0004` = six commits, `46dead0..e2a0b3d`
  - merged: nothing. The branch is left unmerged for `verify` and then `review-close`
- **Status:** `in-progress` → `verifying`
- **Result:** The send-back is fixed. `docs/architecture/overview.md` is at version 5 with `person delete` and `expense delete` described in the body as delivered, ADR-0007's invariant stated where the code enforcing it is described, and the count of new `store.py` functions corrected from two to three against `grep -n "^def "` rather than against the plan's summary. No code, test or acceptance criterion changed; the suite is the same 120 tests and still green on the branch head. `verify` should note that its previous verification at `f4e8319` covered code that has not moved since — the only commit added is a document.

## 2026-08-27T01:39:56Z — verify v0.1.3 — qa-engineer

- **Item:** WI-0004
- **Trigger:** status `verifying`, dispatched by `next`. **Second** verification of this item: the first passed at `f4e8319`, `review-close` rejected on Definition of Done D7 and D12, and `implement` returned it here after fixing `docs/architecture/overview.md`.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the eight acceptance criteria, **read before anything else and before the implementation report**, because they are this skill's only standard
  - `tracker/items/WI-0004/history.md` — ten rows; the branch head verified is `beb522ed117436107fd317c850a85d46782260d5`
  - `tracker/items/WI-0004/artifacts/plan.md` (steps 1–11), `impl-report.md` (round 1 and round 2), `review.md` (F1–F5), and the previous `verify-report.md`
  - `tracker/project.yaml` — `commands.test`, `commands.lint` (null)
  - the branch head `beb522e` itself: `expenses/store.py`, `expenses/cli.py`, `README.md`, `docs/architecture/overview.md` v5
- **Decisions:**
  - **Nothing was inherited.** All eight checkboxes in `item.md` were already ticked when this execution started — the previous verification ticked them. Each criterion was re-derived from its own text and re-demonstrated with commands run in this session before it was left ticked. Leaving a tick in place on the strength of a previous report would be the failure this skill's central gate exists to prevent, and it would be indistinguishable in the record from real work.
  - **The code did not change, and that was established rather than assumed.** `git diff --stat f4e8319..HEAD -- expenses/ tests/ README.md` is empty: the three commits since the first verification are `af331b8` and `beb522e` (tracker) and `e2a0b3d` (`docs/`). That explains why the criteria still pass; it is not a reason to skip checking that they do, and they were all re-run.
  - **`docs/architecture/overview.md` v5 was inspected but not judged.** No acceptance criterion covers it — AC8 is about `README.md` — so verify cannot pass or fail it. The observations were recorded for `review-close`, whose D7 and D12 it is: `version: 5` with a change-log row naming the item; `grep -c "two new functions"` → **0**; the `store.py` piece names three functions and `grep -n "^def " expenses/store.py` returns exactly those three; `## What is coming` now holds WI-0003 alone. Stating a verdict on D7 would have pre-empted the reviewer, and a verifier who grades the Definition of Done leaves nobody checking the grade.
  - **No defect, so no classification call to make.** Nothing failed this item's criteria (which would be a send-back) and nothing delivered by WI-0001 or WI-0002 was found broken (which would be a bug item with `found-in`). No bug was filed and none was warranted.
  - **AC5 was run as one process then a fresh one, deliberately.** Two shell invocations would both be fresh processes and would test nothing about persistence, so `expenses.cli.main` was called twice inside a single interpreter to produce the "immediately after the deletion" listing, and only then was `python3 -m expenses` run as a subprocess and the two outputs compared.
  - **AC6 was checked positively as well as negatively.** Beyond the byte-comparison the criterion requires, the stored JSON was loaded and every `paid_by`, every `shared_by` entry and every `shares_minor` key was differenced against `data["people"]`: the difference is empty. ADR-0007's invariant is observed in the data, not argued from the code.
  - **No criterion was judged ambiguous**, so no question was filed. Each of AC1–AC8 names a command and an observation, and each resolved to a yes or a no without interpretation.
- **Questions raised:** none
- **Commands:**
  - `git rev-parse HEAD` → 0, `beb522ed117436107fd317c850a85d46782260d5`; `git status --short` → 0, empty
  - `git diff --stat f4e8319..HEAD` → 0 (8 files, all under `tracker/` and `docs/`); `git diff --stat f4e8319..HEAD -- expenses/ tests/ README.md` → 0, **empty**
  - `bash /tmp/v5/run.sh` → AC1–AC4, 31 checks, all PASS (byte comparisons via `od -c`, md5 brackets, `wc -c` on stdout)
  - `python3 /tmp/v5/ac5.py` → **0** — AC5; one-process and fresh-process listings identical for both the person case and the expense case
  - `bash /tmp/v5/ac67.sh` → AC6 and AC7, all PASS; includes the seven AC7 vectors with md5 brackets, the two empty-store cases with `[ -e $S ]`, and the JSON invariant check reporting `names in expenses but not in people: none`
  - `grep -c "person delete" README.md` → 3; `grep -c "expense delete" README.md` → 3; `sed -n '/\$ python3 -m expenses expense list/,/^```$/p' README.md` → the numbered sample; `sed -n '48,72p;108,126p' README.md` → AC8(c) and AC8(d) prose read in full
  - `python3 -m unittest discover -s tests -t .` → **0**, `Ran 120 tests in 1.214s`, `OK`
  - five sensitivity probes, each followed by `git checkout --`: A → `FAILED (failures=3)`; B → `FAILED (failures=5)`; C → `FAILED (failures=4)`; D → `FAILED (failures=2, errors=5)`; E → `FAILED (failures=3)`
  - after the probes: `git status --short` → 0, empty; `python3 -m unittest discover -s tests -t .` → 0, `Ran 120 tests in 1.209s`, `OK`
  - `grep -c "two new functions" docs/architecture/overview.md` → 0; `grep -n "^def " expenses/store.py` → eleven functions, three of them this item's
  - `.claude/agile-skills/scripts/validate-workspace .` → 0; `.claude/agile-skills/scripts/check-verify-freshness WI-0004 wi/WI-0004` → 0, `verified at beb522ed, which is the head of wi/WI-0004`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t .` exit 0, `Ran 120 tests`, `OK`, on `beb522e`)
  - `lint-clean` → **skipped** — `commands.lint` is `null` in `tracker/project.yaml`; ADR-0004 records why. This gate checked nothing and is not a pass; the consequence is declared in `verify-report.md` `## Not verified, and why`
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, 0 errors, 0 warnings)
  - `every-criterion-independently-checked` → **pass** — the report's Criteria table gives, for each of AC1–AC8, a command run in this execution and its actual output. No row cites `impl-report.md`, and none cites the appendix holding the first verification
  - `negative-cases-exercised` → **pass** — AC3's two refusals, AC7's seven vectors and two empty-store cases, AC6's refused deletion and AC2's last-expense boundary were each triggered and their exit codes and stderr recorded
  - `tests-would-fail-without-the-change` (advisory) → **pass** — five probes covering all eight criteria (AC1/AC4/AC5 by C, AC2 by A and C, AC3/AC6 by B, AC7 by D, AC8 by E); every one failed with the behaviour removed and the tree was restored and re-verified clean
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/verify-report.md` — rewritten for this round with `Verified-commit: beb522ed117436107fd317c850a85d46782260d5`; the first report is kept in full as an appendix, its own `Verified-commit` line demoted to a quote so only this round's is machine-readable
  - `item.md` — **no change**: all eight boxes were already ticked and every one was re-demonstrated, so none needed ticking and none needed unticking
  - bug items filed: none
- **Status:** `verifying` → `in-review`
- **Result:** **Pass — all eight criteria met on `beb522e`**, each re-demonstrated by commands run in this execution rather than carried over from the first verification. The code, tests and README are byte-identical to the previously verified state; the only change this round is `docs/architecture/overview.md` v5, which no criterion covers and which is recorded with observations for `review-close` rather than judged here. No defects, no bugs filed, no questions raised.

## 2026-08-27T01:44:25Z — review-close v0.4.0 — reviewer

- **Item:** WI-0004
- **Trigger:** status `in-review`, dispatched by `next`. **Second** review of this item: the first, at `e50dc4f`, rejected it on Definition of Done D7 and D12.
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `history.md` (eleven rows, read as a chain), `journal.md` (**all thirteen entries, in full**), `questions/Q-001.md`
  - `artifacts/plan.md` — `## Approach`, all eleven steps, the AC mapping, the four assumptions, `## Decisions and ADRs`, `## Risks`; `artifacts/impl-report.md` rounds 1 and 2; `artifacts/verify-report.md` this round's and its appendix
  - **the diff**: `git diff main..wi/WI-0004 -- expenses/` read hunk by hunk; `-- tests/` as its class and method list plus the single deleted line; `-- README.md` as its complete +/- set. Not the reports about it
  - `docs/architecture/overview.md` v5, `docs/product/vision.md`, `docs/architecture/adr/ADR-0006-…md`, `ADR-0007-…md`, `tracker/items/EP-001/questions/Q-001.md`, `tracker/project.yaml`
  - the merge result in a detached worktree of `main`
- **Decisions:**
  - **Accept.** All twelve Definition of Done criteria pass, including D7 and D12, which are the two that failed last time. The per-criterion table is in `review.md`; a single verdict would not have satisfied the gate.
  - **The D12 audit was re-done from the citations, not carried over.** Twelve claims, each decided by opening the thing it cites: the three function names against `grep -n "^def " expenses/store.py`; `naming_expenses`' three routes against `store.py:135-141`; the refusal-with-a-count against `store.py:151-155`; "nothing was added to `load`" against a diff with zero deleted lines; `VERSION = 1` against `store.py:15`; three actions per noun against `cli.py:32,34,35` and `:42,53,54`; the position column against `cli.py:139-147`; the renumbering against `store.py:162-166`; WI-0003's parking against `EP-001/Q-001`'s answer; ADR-0007's "settle.py unchanged" against an empty `git diff -- expenses/settle.py`; the vision's delete-not-edit claim against `HANDLERS`; and the layering claim against a diff that adds no import. Twelve true. Re-quoting the previous review's verdicts would have been the exact failure D12 exists for, and this item has already produced one instance of that.
  - **D7 is genuinely closed, not merely edited.** `overview.md` is `version: 5` with a change-log row naming the item, the deletion commands are in `## The pieces, and why each exists`, `## What is coming` holds WI-0003 alone, and `grep -c "two new functions"` → 0. `README.md` moved with the item at plan step 10 and `docs/product/vision.md` needed no change — its deletion sentence was written forward-looking and is now simply true.
  - **The trial merge was isolated properly this time.** `git worktree add --detach /tmp/trial5 main`, and `git rev-parse --short main` was checked after the merge and was still `441a9b0`. The first review used `git worktree add /tmp/trial4 main`, which checks out the real branch, and fast-forwarded `main` before it was rewound. That correction is deliberately left in the record rather than tidied away, and the rule is now stated in `review.md` F4.
  - **The order was trial-merge → discard → close → merge**, as the procedure requires. Closing first is what keeps `commits-reference-the-item` meaningful: once the branch is merged, `main..wi/WI-0004` is empty and the gate has nothing to inspect.
  - **Two non-blocking findings, both recorded rather than acted on.** F2: `cli.POSITION_RE` is `^[1-9]\d*$`, so `expense delete 01` is refused with a message true of the form and false of the value — no criterion covers it, `expense list` never prints such a number, and it fails safe. F3: `naming_expenses` still returns positions only `len()` reads, which is the architect's shape and must not be quietly narrowed. Acting on either would be scope no criterion covers.
  - **Six accepted gaps, all written into `item.md`'s `## Notes`.** `lint-clean` checked nothing (ADR-0004, project-wide); AC8(c) and AC8(d) verified by reading only; no criterion pins any refusal message string; F2; F3; and no other platform, older dataset or concurrent use tested. Accepting a gap without writing it where it survives the item is how a paper trail stops being true — once `done`, nobody opens a verification report again.
  - **No bug item filed and no question raised.** Nothing found belongs to another item, and nothing in the change contradicts an ADR, so there was nothing to escalate.
  - **The engagement is not over.** `scripts/engagement-state EP-001` → `active`, `still in flight: BUG-0001, BUG-0002` after this close. No sign-off question is due, and filing one would be ending an engagement that is still running.
- **Questions raised:** none
- **Commands:**
  - `.claude/agile-skills/scripts/check-verify-freshness WI-0004 wi/WI-0004` → 0, `verified at beb522ed; wi/WI-0004 has moved to 2c96f8ea but only the record changed (5 file(s) under tracker/ or docs/)`
  - `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0, `all 8 commit(s) on main..wi/WI-0004 name WI-0004`
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0, `0 errors, 0 warnings`
  - `git diff main..wi/WI-0004 -- expenses/` → 0, read in full; `-- expenses/settle.py` → 0, **empty**; `| grep -E "^\+import|^\+from"` → no import added
  - `grep -c "^- \[x\] AC" tracker/items/WI-0004/item.md` → 8; `grep -c "^- \[ \] AC"` → 0
  - `grep -c "two new functions" docs/architecture/overview.md` → 0; `grep -n "^def " expenses/store.py` → eleven, three of them this item's
  - `git worktree add --detach -q /tmp/trial5 main` → 0; `git -C /tmp/trial5 rev-parse --abbrev-ref HEAD` → `HEAD` (detached, as intended)
  - `git -C /tmp/trial5 merge --no-edit wi/WI-0004` → 0, clean, 13 files changed; `git rev-parse --short main` immediately after → `441a9b0`, unmoved
  - `python3 -m unittest discover` on the merge result → **0**, `Ran 120 tests in 1.215s`, `OK`
  - `git worktree remove --force /tmp/trial5` → 0; `git worktree list` → one entry; `git rev-parse --short main` → `441a9b0`
  - `.claude/agile-skills/scripts/engagement-state EP-001` → `EP-001 active`
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, `0 errors, 0 warnings`
- **Gates:**
  - `definition-of-done` → **pass** — the twelve-row D1–D12 table in `review.md`, each with its own result and evidence
  - `verification-postdates-the-code` → **pass** — `check-verify-freshness` exit 0, by the script rather than by eye; independently, `git diff --stat beb522e..2c96f8e -- expenses/ tests/ README.md` is empty
  - `commits-reference-the-item` → **pass** — `check-commit-refs` exit 0, all 8 commits, run while the branch was still unmerged
  - `tests-pass-on-the-merge-result` → **pass** — `Ran 120 tests in 1.215s`, `OK`, on the detached trial merge, not on the branch
  - `workspace-valid` → **pass** — `validate-workspace .` exit 0
  - `record-is-reconstructible` → **pass** — from the tracker, `docs/` and `git log --grep WI-0004` alone: what was built (`impl-report.md`, both rounds), which skill decided what (eleven history rows, thirteen journal entries, actors named), what was asked and answered (`Q-001`, `answered-by: human`, `## Consequences` naming files that exist and carry the answer), what verification found (two `verify-report.md` rounds with commands and output), and what review judged (this file, twice, with the rejection kept)
  - `claims-are-sourced` → **pass** — `lint-claims --changed-since main` exit 0. That proves the citations resolve; the twelve-row audit is the half no program can do
  - `epic-sign-off` → **not applicable to this move** — this is a work item, not the epic. `engagement-state EP-001` → `active` (BUG-0001 and BUG-0002 still in flight), so no sign-off is due and none was filed
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/review.md` — rewritten for this round with `## What I examined`, the twelve-row claim audit, the D1–D12 table and findings F1–F6; the rejecting review kept in full as an appendix, its correction included
  - `tracker/items/WI-0004/item.md` — `## Notes` gains "What review accepted as gaps, at close", six gaps; `outcome: delivered`
  - merge commit: the branch merged into `main` **after** this transition, per step 8's ordering
  - bug items filed: none; sign-off question: none — the engagement is `active`
- **Status:** `in-review` → `done`
- **Result:** **Accepted, delivered, and closed.** Twelve of twelve Definition of Done criteria pass; the two that rejected this item last time are closed at the root, with `docs/architecture/overview.md` v5 and a claim-by-claim audit done from the citations rather than from the previous verdicts. `person delete <NAME>` and `expense delete <NUMBER>` ship, with `expense list` numbering its lines, and the invariant that no stored expense may name somebody `person list` does not show is now enforced where data is written. Six gaps are accepted and recorded in the item so they outlive the report that declared them. The epic stays `open`: BUG-0001 and BUG-0002 are still in flight.

## 2026-08-27T01:45:07Z — review-close v0.4.0 — reviewer

- **Item:** WI-0004
- **Trigger:** an addendum to the entry immediately above, written by the same `review-close` execution. No status change: the item stays `done`, where that entry left it.
- **Inputs read:** `git log --oneline -3 main`; `git branch --show-current`; the entry above, whose `**Artifacts:**` bullet promised a merge commit it could not yet name
- **Decisions:**
  - **Recording the merge commit by sha, because the previous entry could not.** The procedure's order is trial-merge → discard → close → merge, so the closing entry is always written *before* the merge exists. That leaves "merge commit: …" as a promise rather than a fact, and a reader reconstructing this item from `git log --grep WI-0004` would have to infer which commit it was. It is **`3fa80d4`**, `merge: WI-0004 — person delete and expense delete (refs WI-0004)`, a `--no-ff` merge of `wi/WI-0004` (`f6af696`) into `main` (`441a9b0`).
  - **`--no-ff` deliberately.** A fast-forward would have left no commit saying the item was merged, and this item has already been bitten once by a fast-forward that moved `main` without anybody meaning it to. A merge commit makes the join visible in `git log --graph` and gives `git log --grep WI-0004` a final row that names the event.
  - **The branch `wi/WI-0004` is left in place.** Nothing in the record depends on deleting it, and it is the only copy of the pre-merge history.
- **Questions raised:** none
- **Commands:**
  - `git commit` on `wi/WI-0004` → 0 → `f6af696 tracker: the review, the accepted gaps, and the closed item (refs WI-0004)`
  - `git checkout main` → 0; `git merge --no-ff --no-edit wi/WI-0004` → 0 → `3fa80d4`
  - `python3 -m unittest discover -s tests -t .` **on `main` after the merge** → 0, `Ran 120 tests in 1.200s`, `OK`
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, `checked 7 item(s), 9 document(s)`, `0 errors, 0 warnings`
- **Gates:**
  - `tests-pass-on-the-merge-result` → **pass, re-run on the real merge** — the closing entry recorded this against the detached trial merge, which is what the procedure asks for; this is the same check against `main` itself, `Ran 120 tests`, `OK`
  - `workspace-valid` → **pass** — exit 0 on `main` after the merge
  - every other gate → **unchanged from the entry above**; this addendum records a sha and re-runs two checks, and judges nothing
- **Artifacts:**
  - `main` — advanced from `441a9b0` to `3fa80d4` by a `--no-ff` merge of `wi/WI-0004`
  - `wi/WI-0004` — unchanged at `f6af696`, left in place
  - no file under `tracker/` or `docs/` was changed by this addendum beyond this journal entry itself
- **Status:** `done` → `done`
- **Result:** The merge the closing entry promised is `3fa80d4`, a `--no-ff` merge of `wi/WI-0004` into `main`. The suite passes on `main` after it and the workspace validates. WI-0004 is delivered, merged and closed; `git log --grep WI-0004` now returns the item's whole story, ending with the merge.
