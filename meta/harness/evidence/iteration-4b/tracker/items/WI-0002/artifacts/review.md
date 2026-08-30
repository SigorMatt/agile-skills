# Review — WI-0002

**Verdict: accepted, merged, closed.** This is the **second** review of this item. The first
rejected it on **D12** — a claim in `docs/process/using-recall.md` that the code did not support
— and that finding is fixed. All twelve Definition of Done criteria pass. Three findings are
recorded and accepted rather than blocking, and each is written into the item's `## Notes`; the
line I drew between them and a rejection is stated below, so it can be disagreed with.

The first review's full text, including its D12 claims-audit table and the rejection, is
preserved in git: `git show d479eac:tracker/items/WI-0002/artifacts/review.md`.

## What I examined

- **The whole diff, hunk by hunk**, `main..wi/WI-0002` (`d2ca976..1d4859a`) — not the reports
  about it. `recall/cli.py` (+115), `recall/deck.py` (+54), `recall/store.py` (+33),
  `tests/support.py` (+63), `tests/test_review.py` (+286), `docs/process/using-recall.md`
  (+68/−21). Every hunk traces to an acceptance criterion or a numbered plan step; where it is
  not one-to-one it is discussed in `## Findings`.
- **The incremental diff since the rejection**, `d479eac..1d4859a` over source and docs: four
  hunks in two files — the frontmatter version bump, the corrected paragraph, its change-log row,
  and F2's comment move. Nothing else was touched, which is what a send-back for one finding
  should look like.
- **The record's mechanics, computed rather than eyeballed.** `history.md` has **11** rows and
  chains without a gap (checked in Python: every row's `from` equals the previous row's `to`, and
  row 1's `from` is `—`); its last row's `to` is `in-review`, matching `item.md`. `journal.md`
  carries **14** entries against those 11 rows; the three extras are accounted for individually —
  an `answer-questions` execution at 01:41:39Z that amended this item while consuming EP-001's
  answers, `plan`'s correcting entry at 02:42:34Z adding the seventh gate it had omitted, and
  `implement`'s opening entry at 03:07:42Z, which had no transition to attach to because the
  send-back had already put the item at `in-progress`. All three are legal and all three say so.
- **`journal.md` in full** — all fourteen entries, read end to end rather than skimmed, because
  D5 and `record-is-reconstructible` are certified from it.
- **`verify-report.md`** in full, including `## Not verified, and why`, and **`impl-report.md`**
  in full, including `## What I did not do` and its two-execution structure.
- **`plan.md`** — `## Approach`, the interface list, the AC mapping table, and all five
  `## Assumptions`.
- **The ADRs, at the clauses the code cites**: `ADR-0006` in full; `ADR-0002` `## Decision`
  §1–§7; `ADR-0004` §1–§6; `ADR-0001`'s cited sections. No hunk contradicts a recorded decision.
- **`docs/product/vision.md`** and **`docs/architecture/overview.md`**, for claims about the
  behaviour this item touched that live outside the file the item changed. D12 is not scoped to
  the file with the diff in it.
- **The D12 claims audit, from the citations rather than from the prose** — the table below.

### The D12 claims audit

For each claim, the cited thing was opened and read, and where a command could settle it, the
verification's own evidence at `c50694d` was used rather than a description of it.

| claim | what I opened | verdict |
|-------|---------------|---------|
| the two answers are `y` for right and `n` for wrong | `plan.md` §"The two recognised responses"; `cli.py` `RIGHT_RESPONSE`/`WRONG_RESPONSE` | supported |
| two of them, and no scale in between | `ADR-0002` §Decision 1, *"Two answers, not a scale"*; `GRADE_RESPONSES` has exactly two keys | supported |
| capital letters and surrounding spaces are fine | `_read_grade`: `line.strip().casefold()`; `  Y  ` accepted in verification | supported |
| anything else re-asks the same card | `WI-0002` AC3; `_read_grade`'s loop; demonstrated | supported |
| due means today **or earlier** | `WI-0002` AC13; `due_positions` (`card.due <= today`); today−7 presented | supported |
| a card you add today is due today | `WI-0002` AC12; `new_card(due=today)`; demonstrated | supported |
| **everything** that is due, no cap, no timer | `WI-0002` AC11; `due_positions` returns every match and nothing slices it; 60 of 60 presented | supported |
| answers are written down as you give them | `WI-0002` AC9; `store.save` **inside** the loop; an abandoned sitting kept its answer | supported |
| `Ctrl-D` at either prompt stops the sitting | `_read_line` catches `EOFError`, and it is the reader at both reads | supported |
| nothing due is not an error, and exits successfully | `WI-0002` AC5; the early `return EXIT_OK`; exit 0 observed | supported |
| the same line when you have no deck yet | `ADR-0004` §6 (*"Absent is not the same as unreadable"*); `WI-0002` AC6; the two stdouts are byte-identical | supported |
| a sitting never creates the deck file | `store.load` never writes; the nothing-due branch returns before any `save`; `find` over the home found **0 entries** afterwards | supported |
| `add`, `list` and `review` all refuse a damaged deck and leave its bytes alone | `ADR-0004` §5; the single `_report_unreadable` call site in each; eight damaged decks, `sha256` identical either side | supported |
| **the corrected paragraph** — answers are written into the deck file `[src: ADR-0006]` | `ADR-0006` §1 (`grade` records the most recent answer) and §4 (written only when set); the graded decks verification produced | **supported** |
| **the corrected paragraph** — nothing reads them back; `record_answer` leaves the ladder position exactly as it was `[src: recall/deck.py:92]` | `deck.py:92–102` — `dataclasses.replace(card, grade=…, due=today+1)`, `rung` absent from the call; `grep -rn "rung" recall/` shows the only other mentions are `store`'s round-trip; a card planted at `rung: 2` and answered **right** was still at `rung: 2` afterwards | **supported** |
| **the corrected paragraph** — every card is still on the bottom rung `recall add` put it on `[src: recall/deck.py:73]` | `deck.py:73` — `rung=FIRST_RUNG`, and `FIRST_RUNG = 0` | **supported, with F3 below** |
| **the corrected paragraph** — that is where it will start climbing from when the ladder lands | follows from the row above; `ADR-0006` `## Consequences` says WI-0003 changes `rung` and `due`. Hedged on WI-0003 landing, and declared unverifiable in `verify-report.md` | supported |
| `overview.md` — a card carries how it went last time, once reviewed | `ADR-0006` §1; `store._card_to_entry` | supported |
| `overview.md` — `cli.py` is, since `review`, the **only** layer that reads standard input | `grep -rn "input(\|sys.stdin" recall/ bin/` → exactly one hit, `recall/cli.py:198` | supported |
| `overview.md` — `review` saves the deck after every graded card | `cmd_review`'s loop body; AC9 demonstrated | supported |
| `vision.md` — a card is graded right or wrong and the gap walks the ladder 1, 3, 7, 30 | `EP-001/Q-003` and `ADR-0002` §2. **Not a claim about today's code**: it is the stakeholder's own statement of what they want, quoted with a return address, in the document that states the target product. `using-recall.md` is where what is *built* is stated, and it now says the ladder is not built. Under `ADR-0008` this sentence is theirs and is not mine to repair | supported, and out of D12's reach |

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c '^- \[ \] AC'` = **0**, `grep -c '^- \[x\] AC'` = **13** |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | thirteen rows in `## Criteria`, each with the command the verifier ran and its quoted output. The report states in terms that no verdict rests on `impl-report.md`, and no row cites it. Crucially the second verification **re-ran all thirteen** rather than carrying the first's evidence forward — correct, because AC3, AC5 and AC6 are decided by reading the document this send-back changed |
| D3 | gates passed on the **final** state of the code | **pass** | `implement`'s closing gates ran on `ef7a00d`, the last code commit; `verify`'s on `c50694d`; the only commits after that are `1d4859a` and this close, both `tracker/`-only. Confirmed with `git diff --name-only c50694d..HEAD` → five paths, all under `tracker/` |
| D4 | no open blocking question | **pass** | `Q-001`, `Q-002` both `status: answered`, both with `## Consequences` naming files I opened |
| D5 | a journal entry per execution; history chains | **pass** | 11 rows, chain verified in Python; 14 entries; the three extras named individually in `## What I examined` |
| D6 | design decisions in an ADR, cited from plan or journal | **pass** | `ADR-0006` created by `plan`, cited from `plan.md` §"Decisions and ADRs" and from `store.py`/`deck.py` at each clause it governs. The decisions this send-back involved — that the placeholder banks nothing — are `plan.md` §Assumptions, cited from `record_answer`'s docstring |
| D7 | invalidated documents updated, with a version bump and a change-log row | **pass** | `using-recall.md` v2 → v3 → **v4**, two change-log rows, the second naming F1 and what was wrong with the old sentence. `overview.md` v1 → v2 and `ADR-0002` v1 → v2 were bumped earlier in the item. See **F2**: two documents carry a stale *enumeration*, which is not the same as an invalidated claim, and the distinction is argued there rather than assumed |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → `all 15 commit(s) on main..wi/WI-0002 name WI-0002`, exit 0 |
| D9 | merged into the trunk | **pass** | trial merge into a **detached** worktree of `main` produced `24628a1`, clean, with the suite green on it (`Ran 32 tests in 3.471s` / `OK`, exit 0, run **inside** the trial). `main` was `d2ca9768…` before the trial and `d2ca9768…` after — the trial published nothing, and `git worktree list` shows no leftover. The real merge is performed immediately after this close, in the order the procedure requires: `commits-reference-the-item` reads `main..branch`, which merging empties, so closing must come first. The merge commit's sha is recorded in this item's journal |
| D10 | `verify` ran **after** the last code change | **pass** | `check-verify-freshness WI-0002 wi/WI-0002` → *"verified at c50694d4; wi/WI-0002 has moved to 1d4859a4 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*, exit 0. Compared mechanically, and cross-checked by listing the changed paths myself |
| D11 | `review.md` states what was examined | **pass** | this document, `## What I examined` first, with the claims audit as a table of what was opened |
| D12 | every claim in `docs/` about the touched behaviour is still true, read against the code | **pass** | the twenty-one-row audit above, run from the citations. The one claim that failed last time is fixed and now supported by both things it cites. Three documents were audited, not one: `using-recall.md`, `overview.md` and `vision.md` |

## Findings

### F1 — accepted, recorded. A source docstring overclaims conformance to `ADR-0002`

`recall/deck.py:100`, in `record_answer`'s docstring:

> For a wrong answer this already is ADR-0002's rule.

and `plan.md` §Assumptions, the sentence it derives from:

> for a *wrong* answer it is already the real rule, exactly [src: ADR-0002], so WI-0003 only has
> to add the right-answer ladder walk

**Why it is not true.** `ADR-0002` §Decision 6 is: *"Wrong sends the card back to the first
rung, so its next review is one day after the day it was reviewed."* Two clauses. The placeholder
satisfies the second — `due = today + 1` — and not the first: `rung` is left exactly as it was,
deliberately, which is the point of the whole assumption. So the placeholder matches ADR-0002's
rule on the **date** and not on the **rung**.

**What would go wrong and when.** WI-0003 is the next item and depends on this one. Its author
reads *"WI-0003 only has to add the right-answer ladder walk"*, implements the ladder walk for
right answers, and leaves wrong answers alone — because they were told the wrong-answer case was
already correct. The result is a card that is answered wrong and stays on rung 4, exactly the
defect `ADR-0002` §6 exists to prevent.

**Why accepted and not a rejection.** Three reasons, and they are specific rather than general
leniency:

1. **It is not in `docs/`**, so D12 does not reach it; it is a step-4 finding about code I would
   have to maintain.
2. **It breaks no acceptance criterion.** This item's `## Out of scope` says in terms that the
   forward step is *"a placeholder WI-0003 replaces"* and asks only that the card stop being due
   for the rest of the day, which it does.
3. **The function is the thing WI-0003 deletes.** `plan.md` says `record_answer` *"is where
   WI-0003 will land"*. Rewording a docstring that is about to be replaced protects nobody; what
   protects WI-0003's author is a note on the item they will read as their dependency. That is
   where it has gone.

**Recorded in `## Notes`** with the correction spelled out, so WI-0003's plan meets it before its
author meets the docstring.

### F2 — accepted, recorded. Two documents carry a stale enumeration

This item added a third subcommand, and two sentences written when there were two have not
caught up:

- `ADR-0004` §5: *"In that case **both subcommands** report the path on standard error and exit
  non-zero, and neither writes anything."* There are now three, and all three do.
- `docs/architecture/overview.md`, §"Why it is split that way": *"…lets the same load path serve
  `add`, `list` and, **later**, `review`…"* `review` is no longer later.

**Why this is not a D12 failure and not a D7 failure.** The distinction I am drawing, stated so
it can be argued with: **a claim whose substance is still true but whose incidental enumeration
has aged is stale, not false.** A reader of `ADR-0004` §5 learns the rule correctly — a deck that
cannot be read is never repaired — and a reader of `overview.md` learns the split correctly. Both
sentences *understate*; neither misleads, and no reader acts wrongly on either. That is exactly
the line the first review drew when it rejected: the sentence it rejected told a person their
effort was being banked when it was not, and they would have acted on it. Nobody acts on a
subcommand count.

`overview.md`'s reading is defensible outright — the section narrates why the split was made, and
*"later"* is true of the build order, which is what a design rationale is about.

Recorded in `## Notes` with both one-clause fixes named, so the next item touching either file
takes them.

### F3 — accepted, recorded. `verify`'s observation O1, decided here

`verify` raised, correctly, that *"Every card is still on the bottom rung `recall add` put it
on"* is an absolute claim defeasible by hand-editing the deck file, which `ADR-0004` contemplates
by choosing JSON. It declined to decide it and put it to me, which is the right routing — D12 is
mine.

**Decided: supported, no change required.** The claim's citation, `recall/deck.py:73`, supports
exactly what the sentence asserts about the population it is about: every card `recall add`
creates starts at `FIRST_RUNG`, and nothing in `recall/` moves it. A person who set a rung by
hand is outside the sentence's population and is not misled by it — and the sentence's operative
promise, *"that is where it will start climbing from when the ladder lands"*, holds for their
card too. Recorded in `## Notes` with the one-word tightening (*"every card `recall add` made"*)
named, in case a later reader prefers it.

### Nothing else

No hunk in `recall/` or `tests/` fails to trace to a criterion or a numbered plan step. No hunk
contradicts an ADR; every `ADR-nnnn section n` citation in the new code says what the ADR says,
and I opened each. The three helpers in `tests/support.py` not in `plan.md`'s interface list —
`days_from_today`, `stored_cards`, `NOTHING_DUE_MARKER` — are test machinery serving criteria the
plan does name, and `NOTHING_DUE_MARKER` mirrors the existing `EMPTY_DECK_MARKER` device. Not a
finding. The three declared deviations in `impl-report.md` are all "how" and each reversible in
one line; I judged each and accept all three, the `stdin` default in particular, which turns a
test that forgets its input from a hang into a failure.

## Accepted gaps

Each is written into the item's `## Notes`, because a gap recorded only in a report stops being
read the moment an item closes. The four the first review recorded are already there and stand;
these three are added.

1. **F1** — the wrong-answer conformance overclaim, above. The one WI-0003 must not inherit.
2. **F2** — the two stale enumerations, above.
3. **F3** — the hand-edited-rung qualification, above.
4. **`BUG-0001` is untouched, and a passing AC7 is not evidence about it.** `review` reaches the
   deck through the same `store.load` as `add` and `list`, so it inherits the same weakness with
   filesystem errors that are not deck-*content* problems. `plan.md` §Risks requires leaving it;
   the bug is open at `ready`. `verify` was right not to re-file it — a duplicate would split its
   verification.
5. **The placeholder schedule is invisible to a person using the tool** — a card returns tomorrow
   whether they got it right or wrong. Accepted because the item excludes the ladder, and it is
   the reason the documentation paragraph had to be *accurate* rather than merely present. It now
   is.
6. **No injectable clock**, so a sitting spanning midnight is unexercised and a suite started
   seconds before midnight can flake. In `plan.md` §Risks; no criterion covers it.
7. **Presentation order is deck order and no criterion constrains it.** `refine` left it
   unconstrained deliberately and `plan.md` chose it with the reversal cost recorded. A later
   change would break no criterion of this item.

## Verdict

**Accepted.** The rejection is answered: the sentence that told a person their reviewing effort
was being banked towards the schedule is gone, and what replaces it is supported by both things
it cites and by decks the verification produced — a card planted at `rung: 2` and answered right
was still at `rung: 2`, and a card answered wrong was still at `rung: 0`. F2's stranded comment
now sits on the prompts it governs, and the AC1 mutation confirms the guard it describes is still
enforced by a test.

All thirteen acceptance criteria hold and were **independently re-demonstrated** at `c50694d`,
not carried forward — which was the right call, because three of them are decided by reading the
document that changed. Twelve Definition of Done criteria pass. Three findings are recorded and
accepted, with the line between accepting and rejecting argued in F2 rather than assumed.

The item is closed `done` / `delivered` and `wi/WI-0002` is merged into `main`.
