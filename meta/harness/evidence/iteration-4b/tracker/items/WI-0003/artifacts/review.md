# Review — WI-0003

## What I examined

- **`item.md`** — the six criteria and their tick state, `## Out of scope`, and the whole of
  `## Notes` including the two questions routed to `plan` and the two things inherited from
  `WI-0002`'s closing.
- **`history.md`** — eight rows, chaining `draft → awaiting-answer → draft → ready → planned →
  in-progress → verifying → in-review` with no gap, the last row matching `item.md`'s status.
- **`journal.md`** — read in full, all nine entries: `intake`, `answer-questions` (the epic's
  answers reaching this item), `refine` round 1, `answer-questions` (Q-001, Q-002), `refine`
  round 2, `plan`, `implement` opening, `implement` closing, `verify`.
- **`plan.md`**, **`impl-report.md`**, **`verify-report.md`** — in full, including
  `## Deviations from the plan`, `## What I did not do` and `## Not verified, and why`.
- **`questions/Q-001.md` and `Q-002.md`** — both `answered`, `answered-by: human`, both with a
  `## Consequences` section naming files I opened: `ADR-0002` (v3), `ADR-0007` (new),
  `docs/product/vision.md` (v4), this item's `## Notes` and `refinement-qa.md`.
- **The diff, `main..wi/WI-0003`, hunk by hunk** — 8 commits, 13 files: three source files, two
  test files, two documents, and the tracker.
- **The ADRs the change rests on** — `ADR-0002` (the ladder), `ADR-0004` (the deck file),
  `ADR-0006` (the grade), `ADR-0007` (the printed line), `ADR-0008` (what `rung` counts).

### The claims audit, from the citations

D12's read, done the one way that can fail: each absolute claim the delivered work touched was
taken to **the thing it cites**, and the verdict comes from what was there.

| claim | in | what I opened | verdict |
|-------|----|---------------|---------|
| *"It is where the scheduling rule belongs, and WI-0003 put it there"* | `overview.md` §layers | `recall/deck.py` — `LADDER` at line 24, `record_answer` implementing the rule | true |
| *"The ladder's four numbers exist there once and nowhere else"* | `overview.md` §layers | `grep -rnE "timedelta\(days=[0-9]+\)\|\b(1, 3, 7\|3, 7, 30)\b" recall/*.py` → one hit, `recall/deck.py:24` | true |
| *"a card's … ladder position [is refused rather than silently corrected]"* | `overview.md` property 1 | `recall/store.py` `_card_from` — the range check raising `DeckUnreadable`; and by command, a stored `rung` of `9` → exit 3, deck bytes unchanged | true |
| *"The gaps are 1 day, then 3 days, then a week, then 30 days … never grows past a month"* | `using-recall.md` | `ADR-0002` §2 and §5, then `LADDER` and the `min(…)` in `record_answer` | true |
| *"a wrong answer … due again the day after the sitting … moves one day out again rather than a month"* | `using-recall.md` | `ADR-0002` §6; `record_answer`'s wrong branch; and the AC2(b) run | true |
| *"Both gaps are counted from the day of the sitting, never from the day the card was due"* | `using-recall.md` | `ADR-0002` §4 and §6 (*"after the day it was reviewed"*); `record_answer` adds to `today` | true |
| *"due on days 0, 1, 4, 11, 41, 71 and 101"* | `using-recall.md` | `ADR-0002`'s own worked line — *"day 0 (added), then +1, +4, +11, +41, +71, +101"* | true |
| *"`recall list` prints `question \| answer` and no dates"* | `using-recall.md` | `ADR-0007` §4; `cmd_list`, untouched by the diff | true |
| *"There is no tally or summary at the end of a sitting"* | `using-recall.md` | `ADR-0007` §3; `cmd_review` prints only per-card | true |
| *"The date it names is the one written into the deck file for that card"* | `using-recall.md` | `_next_review_line` formats `card.due`, and verification compared the printed string against the stored one on four sittings | true |
| *"There is no way to change the four gaps …"* | `using-recall.md` | `WI-0003` `## Out of scope`, first and last bullets | true |
| *"Nothing keeps a record of past sittings: the deck file holds how the last one went and no more"* | `using-recall.md` | `ADR-0006` §1 — *"It records the most recent answer, not a history"*; `_card_to_entry` writes one `grade` | true |

`lint-claims --context work-item --changed-since main` → exit 0 over a scope that could have
found something: *"2 document(s) in 2 path(s) differ from main (a798a5e) under docs"*. Not a
window that examined nothing.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every checkbox ticked | **pass** | `grep -c "^- \[x\] AC" item.md` → 6, and there are six criteria. None was ticked by `implement`; all six were ticked by `verify` after its own runs |
| D2 | every tick cites its evidence | **pass** | `verify-report.md`'s criteria table has one row per criterion, each naming the command run and quoting its actual output. Spot-checked three by re-reading the quoted output against what the criterion asks: AC1's `[1, 3, 7, 30, 30]`, AC2(b)'s `then right -> today + 1`, AC4's four distinct printed dates |
| D3 | gates passed on the **final** state | **pass** | `implement`'s eight gates ran after its last source commit; `verify` re-ran the two command gates itself on `c2c547a`; I ran them again on `d5fa9aa` and on the **merge result** (`196df9a`), all exit 0 |
| D4 | no open blocking question | **pass** | Both questions on the item are `status: answered`, `answered-by: human`, with `## Consequences` naming files that exist. Workspace-wide, `grep -rl "^status: open" tracker/items/*/questions/` returns nothing |
| D5 | an entry per execution, history chains | **pass** | Nine journal entries against eight history rows; the extra is `answer-questions` at 01:41:39Z, an execution that propagated the epic's answers into this item without moving it — an entry with no row is legal, a row with no entry is not, and there is none. `validate-workspace` → 0 errors |
| D6 | every design decision in an ADR, cited | **pass** | `ADR-0008` records what `rung` counts and what an out-of-range one does, and is cited from `plan.md`'s `## Decisions and ADRs` table and from `journal.md`. `ADR-0007` and `ADR-0002` carry the stakeholder's decisions and are cited from the plan. Nothing in the diff decides something no ADR or plan assumption records — the printed line's wording is `plan.md` `## Assumptions` 1–2, declared |
| D7 | invalidated documents updated, with a version bump and a change-log row | **pass** | `docs/process/using-recall.md` v4 → **v5**, change-log row present, and the section claiming scheduling was unbuilt is gone. `docs/architecture/overview.md` v3 → **v4**, change-log row present, restating two commissive clauses as description. Both bumps carry `updated-by` and `updated-for: WI-0003` |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → *"all 8 commit(s) on main..wi/WI-0003 name WI-0003"*, exit 0 |
| D9 | merged into the trunk | **pass** | Trial merge into a **detached** worktree of `main` produced `196df9aadd57306cbc0a8fb0a9fcb854eaceb895`, clean (13 files, 915 insertions), with `python3 -m unittest discover -s tests -t . -q` run **inside** the trial → `Ran 43 tests … OK`, and `compileall` exit 0. `main` was `a798a5e5…` before the trial and `a798a5e5…` after, so the trial published nothing. The real merge follows this close, in the order the procedure requires: `commits-reference-the-item` reads `main..branch`, which merging empties. The real merge landed as `fb8b98194ee5308061d86086ad5b88da1843f9ee` on `main`, with the suite green on it (`Ran 43 tests … OK`) and `validate-workspace` at 0 errors; `git log --grep WI-0003` returns it |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0003 wi/WI-0003` → *"verified at c2c547ac; wi/WI-0003 has moved to d5fa9aa0 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*, exit 0. Cross-checked by hand: `git diff --stat c2c547a..d5fa9aa` touches only `tracker/` |
| D11 | `review.md` states what was examined | **pass** | This document, `## What I examined` first, including the twelve-claim audit table above |
| D12 | claims about the behaviour this item touched are still true | **pass, with one finding recorded** | The audit table above: twelve claims, each read against the thing it cites, all twelve true. The finding below is not one of them — it is a claim about the **test corpus**, not about behaviour, which is why D12 passes and the finding is recorded rather than blocking |

## Findings

**F1 — a stale clause in `ADR-0008`'s `## Consequences`, and a gate that will not let this
execution repair it.** Severity: low. Not a send-back.

`ADR-0008` `## Consequences` ends its unit-test bullet with:

> No deck file in any test carries a `rung` other than `0` [src: tests/support.py:135].

That was true when `plan` wrote it and is now false: `LadderStorageTests.test_a_rung_outside_
the_ladder_is_refused_like_any_other_bad_field` writes deck files with `rung` of `-1`, `4` and
`9`, deliberately, to prove §6 refuses them [src: tests/test_review.py:505].

Two judgements about it, and I want both on the record because they pull in opposite directions.

- **Why it is not a send-back.** D12 is scoped to *"claims in `docs/` about the behaviour this
  item touched"*. This clause is about the contents of the test suite at a moment in time, in a
  Consequences section, supporting §7 — that `DECK_FORMAT_VERSION` stays at `1`. §7 is still
  sound for exactly the reason it always was: those decks exist to be **refused**, and no deck
  the tool itself writes carries a `rung` outside the ladder. Nobody is misled about behaviour.
- **Why it is still a finding.** It is a confident absolute sentence that a reader would take at
  face value, and this item is what falsified it.

**I attempted the repair `spec/doc-header.md` §4b provides and reverted it.** Written as an
`erratum` with a `## Corrections` row, a change-log row and a version bump, it made
`cross-answer-consistency` fail: `lint-answers` treats `## Consequences` as one paragraph block,
that block also carries `[src: WI-0003/Q-001]`, and editing any bullet in it reads as rewriting a
stakeholder-sourced claim (`answer.claim-rewritten-unasked`). The escape the tool's own hint
offers — *"cite compatibility in a `**Cross-answer check:**` journal bullet naming
WI-0003/Q-001"* — cannot be taken by the execution making the edit, because `transition` runs its
gates **before** it writes the journal entry that would satisfy them. Forcing a hard gate over a
low-severity stale clause is not a trade this review is willing to make.

**What unblocks it:** this execution's journal entry names `WI-0003/Q-001` on its
`**Cross-answer check:**` bullet — truthfully, because the Q-001-sourced sentence in that block
was read here and is untouched and compatible. `journal_checks()` scans every journal in the
workspace, so the **next** execution that opens `ADR-0008` will find the gate already satisfied
and can apply the §4b erratum in one command. The finding is carried into `item.md` `## Notes` so
it survives this item closing.

**F2 — line-anchored citations decay silently, and this item decayed fifteen of them.**
Severity: low. Recorded, not acted on.

`docs/` carries fifteen `[src: <file>.py:<line>]` citations across `ADR-0006`, `ADR-0007` and
`ADR-0008`. This item shifted `recall/deck.py`, `recall/store.py`, `recall/cli.py`,
`tests/test_review.py` and `tests/support.py`, so most now point somewhere else —
`ADR-0008`'s `[src: recall/deck.py:92]`, written to point at the placeholder `record_answer`,
now lands inside `due_positions`' docstring; `ADR-0006`'s `[src: recall/store.py:112]` now lands
on a bare `raise`.

Nothing fails, and correctly so: `spec/doc-header.md` §4a resolves a workspace-path citation when
**the file exists**, so the line is advisory. But the property §4a exists to buy — a claim
checkable *in one hop* — is what the line number was carrying, and it is gone. Repairing them is
not this item's to do and would be make-work item by item; the durable fix is a convention that
does not anchor to line numbers, or a checker that reads them. Recorded here and in
`HARNESS-STATUS.md` as an observation about the toolkit rather than about this change.

## The diff, read against the plan

Every source hunk traces to a plan step, and I checked each against the criterion or step it
serves rather than against the report:

- `recall/deck.py` — `LADDER` (step 1), `record_answer` rewritten (step 2), `days_until` (step 4's
  explicitly-open interface note), module docstring (declared deviation 4). The docstring change
  is the right call: it said the overview *"puts the scheduling arithmetic here when WI-0003
  arrives"*, which this item makes false.
- `recall/store.py` — the range check in `_card_from` (step 3), placed after the type checks and
  before the date parse, using the same message shape as its siblings. It contradicts no ADR:
  `ADR-0004` §5 refuses to repair an unreadable deck and this refuses rather than clamps, which
  is `ADR-0008` §6 exactly.
- `recall/cli.py` — `NEXT_REVIEW_LINE`, `_next_review_line`, and the `print` after `store.save`
  (step 4). Placing it after the save is `plan.md` `## Assumptions` 3, and I checked the
  consequence it claims: a sitting that grades nothing prints nothing, confirmed in verification's
  boundary cases 1 and 2.
- `tests/` — the placeholder unit test replaced (step 5), `SchedulingTests` and the `set_due`
  helper (step 6), and `LadderStorageTests` (declared deviation 3). The helper asserting that the
  rung it did not touch survives the rewrite is the specific defence `plan.md` `## Risks` asked
  for, and it is there.
- `docs/` — steps 7 and 8, the latter as declared deviation 1.

**Nothing in the diff serves neither a criterion nor a plan step**, and nothing contradicts an
ADR. Would I maintain it? Yes. The one thing I looked hardest at is `record_answer`'s two-branch
shape: it computes the gap and the next rung together, so the "which rung's number applies" question
that `ADR-0008` §2 exists to settle is answered in one place and cannot drift between the date and
the position. That is the failure `WI-0002`'s closing warned this item about.

## Accepted gaps

Each is written into `item.md` `## Notes` as well, so it survives this item closing.

1. **F1 — the stale clause in `ADR-0008` `## Consequences`**, with the repair route and what
   unblocks it. Accepted because D12 is scoped to behaviour and this is a statement about the
   test corpus; recorded because it is nonetheless false.
2. **F2 — fifteen decayed line-anchored citations** across three ADRs. Accepted because §4a's
   resolution rule is satisfied and repairing them per-item is make-work; recorded because the
   one-hop checkability they were carrying is gone.
3. **`overview.md`'s `store.py` bullet still says the load path serves "`add`, `list` and,
   later, `review`"**, though `review` shipped with `WI-0002`. Declared by both `impl-report.md`
   and `verify-report.md` and correctly left alone — it is outside this item's D12 scope and
   fixing it here would have put a hunk in the diff tracing to nothing. One line for whoever next
   opens that file.
4. **The worked example's later days — 41, 71 and 101 — were not observed at calendar distance.**
   Declared in `verify-report.md` `## Not verified, and why`. Accepted: no criterion asks for it,
   it would take a hundred days, and the arithmetic that produces those days was observed
   directly (gaps 1, 3, 7, 30, 30) with AC3 independently establishing that the gap counts from
   the day of the sitting.
5. **`BUG-0001` remains open and untouched.** Correct, and confirmed: the new `DeckUnreadable`
   from an out-of-range `rung` is reported through `ADR-0004` §5's existing route — a message and
   exit 3, not a traceback — which verification's boundary case 5 demonstrates. This item did not
   widen to absorb it and did not make it worse.

## Verdict

**Accept.** All six acceptance criteria are ticked on evidence `verify` gathered itself, all
twelve Definition of Done criteria pass, the merge result is green, and the record is
reconstructible from the tracker, `docs/` and `git log --grep WI-0003` alone. Two findings are
recorded rather than sent back, both low severity, both carried into `item.md` `## Notes` so they
outlive this item. `outcome: delivered`.
