# Review — WI-0004

## What I examined

- **The record's mechanics.** `history.md` — eight rows, chaining without a gap from creation to
  `in-review`, its last row matching `item.md`'s status. `journal.md` — eight entries, read in
  full, one per history row and one per skill execution (`answer-questions` ×2, `refine` ×2,
  `plan`, `implement` ×2, `verify`). Both questions on the item, `Q-001` and `Q-002`: `answered`,
  `answered-by: human`, each with a `## Consequences` section naming files that exist and that
  do carry the change described.
- **The diff, hunk by hunk**, `main..wi/WI-0004` — five files, read as a diff rather than as a
  description of one. Mapped below.
- **The reports.** `impl-report.md` and `verify-report.md` in full, including `## What I did not
  do` and `## Not verified, and why`, and `plan.md`'s ten steps, four assumptions and risk list.
- **`ADR-0009`**, opened rather than cited from memory, to check that what `cmd_delete` does is
  what it decided: the prompt is asked once, anything that is not a yes cancels, and declining
  exits 0. It does, and the ADR is cited from `plan.md`'s decision table and from the code.
- **The D12 claim audit, from the citations.** Each absolute claim this item wrote or touched,
  with the thing it cites opened:

  | claim | cites | what I opened, and what it says |
  |-------|-------|-------------------------------|
  | "the listing is unchanged by this command" | `WI-0004 AC12` | `item.md` AC12, and the diff: `cmd_list` is not in it |
  | "capital letters and surrounding spaces are fine … anything else … leaves the deck exactly as it was" | `WI-0004 AC6`; `ADR-0009` | `ADR-0009` §Decision and `recall/cli.py`: `reply.strip().casefold() != CONFIRM_RESPONSE` |
  | "the question is put **once**" | `ADR-0009` | `ADR-0009`, which decides exactly this and gives the reason `review` differs |
  | "`recall` says how many matched rather than guessing" | `WI-0004 AC5`; `Q-001` | `Q-001`'s answer — *"B — let me just type the question"* — and the refusal path in `cmd_delete`, which formats `len(positions)` |
  | "Two cards may share a question side" | `WI-0001 AC9` | `WI-0001` AC9: *"Adding a card whose question side is identical … is allowed and produces two cards"* |
  | "removing one of such a pair means editing the deck file by hand"; "There is no undo"; "no way to delete more than one card at once" | `tracker/items/WI-0004/item.md` | the item's `## Out of scope`, which says all three |
  | "a deletion never writes a deck file into existence" | `WI-0004 AC9` | AC9, and `cmd_delete`'s ordering: the blank check and both refusals precede any `store.save` |
  | "`add`, `list`, `review` and `delete` all say so, name the file" | `ADR-0004`; `WI-0001 AC8`; `WI-0002 AC7`; `WI-0004 AC8` | `recall/cli.py`: one `_report_unreadable` site, called from all four handlers |
  | "`remove` constructs no card, so no survivor's rung, due date or order can move" | `recall/deck.py`; `WI-0004 AC11` | `recall/deck.py`: `del self._cards[position]`, and nothing else in the method |
  | "an added card starts at the bottom of the ladder and is due today" | `recall/deck.py`; `ADR-0002` | `deck.py`'s `new_card`: `rung=FIRST_RUNG, due=today` |

  One claim did **not** survive that read; it is finding **F1** below.
- **The gate commands**, run here: `lint-claims --context work-item --changed-since main`
  (scope reported by the tool itself as *"2 document(s) in 2 path(s) differ from main (152c531)
  under docs; citations: every markdown file in the workspace"*), `lint-answers --changed-since
  main` (*"claim window: 2 path(s) differ from main"*, 9 consumed human answers checked),
  `check-commit-refs`, `check-verify-freshness`, `engagement-state EP-001`, and the trial merge.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | AC1–AC12 all `- [x]` in `item.md`; `validate-workspace` exit 0 |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | the report's table gives, per criterion, a command run in verification and its quoted output — `exit=2` and the stderr text for AC4, `sha256` before/after for AC4–AC8, `find $HOME -type f → 0` for AC9, the field-by-field JSON comparison for AC11. No row cites `impl-report.md` |
| D3 | gates passed on the final state of the code | **pass** | `implement`'s gates ran on `1d46cae`, the last code commit; `verify` re-ran the suite and the lint itself on `ffef942`; this review ran the suite **on the merge result** (`04c5a38`, 55 tests, OK) and `compileall` (exit 0) |
| D4 | no open blocking question | **pass** | `Q-001` and `Q-002` both `answered`; no other question on the item |
| D5 | a journal entry per execution, history chains | **pass** | eight rows, eight entries, read in full; `validate-workspace` exit 0 |
| D6 | design decisions in an ADR, cited | **pass** | `ADR-0009` records the one interface-visible decision (ask once, declining exits 0) and is cited from `plan.md`'s decision table, from `recall/cli.py`'s constants and `cmd_delete`, and from `docs/architecture/overview.md`. The four cheap-to-reverse choices are `plan.md` `## Assumptions` 1–4, which is where they belong |
| D7 | invalidated documents updated, with a version bump and a change-log row | **pass** | `docs/process/using-recall.md` v6 (new `## Deleting a card`, plus the damaged-deck sentence and the "does not do yet" paragraph this item falsified) and `docs/architecture/overview.md` v6, each with its row. Both bumped again to v7 by this review — see F1 and F2 |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → *"all 4 commit(s) on main..wi/WI-0004 name WI-0004"* |
| D9 | merged into the trunk | **pass** | trial merge in a **detached** worktree of `main` produced `04c5a38fc594496f504c4a238939af243032aca2`, with the suite run **inside** it (`Ran 55 tests … OK`) and `compileall` exit 0; `main` was `152c5318…` before the trial and `152c5318…` after, so the trial published nothing. The real merge followed the close, in the order the procedure requires — `commits-reference-the-item` reads `main..branch`, which merging empties — and landed as `7668ddef109c5f52fd89bc81292ff6da7b0ddfc9` on `main`, with the suite green on it (`Ran 55 tests … OK`), `validate-workspace` at 0 errors and 0 warnings, and `engagement-state EP-001` then reporting `active` with BUG-0001 the only item still in flight |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness` → *"verified at ffef9421; wi/WI-0004 has moved to 3b80a6bc but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*. Reached only after finding **F3** |
| D11 | `review.md` exists and says what was examined | **pass** | this file; `## What I examined` is first and lists the artifacts, the diff range, the ten audited claims with what was opened for each, and the commands run |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass, after a repair** | the audit table above, decided from the cited sources. One claim was false — **F1**, repaired here |

## The diff, read against the plan

`main..wi/WI-0004`, five files. Every hunk traces to a plan step or to a declared deviation:

- `recall/deck.py` — `positions_matching` (step 1) and `Deck.remove` (step 2). Both are values-only
  and neither touches the filesystem, so the layer rule in `docs/architecture/overview.md` holds.
  `positions_matching` is shaped like `due_positions` — selects, decides nothing — which is the
  precedent the plan named. The docstring carries the constraint the plan's risk list asked for:
  a caller must not reload the deck between the match and the removal. Worth maintaining.
- `recall/cli.py` — the subparser (step 3), two constants and the accepted reply (step 4), and
  `cmd_delete` (step 5). The refusal order is the one that makes AC7 and AC9 true by construction
  rather than by care: the blank check precedes `store.deck_path()`, and every refusal precedes
  the prompt. `DeckUnreadable` is caught at the single existing site, so there is no second error
  path to drift. No new exit code, which keeps `ADR-0001` §5's two classes as the whole vocabulary.
  Nothing here contradicts an ADR.
- `tests/test_delete.py` — steps 6 and 7. Twelve tests, one per criterion, driving the real
  binary. The AC6 case is four separate subprocess runs rather than one parameterised call, which
  is what the plan asked for so the end-of-input case crosses the process boundary for real.
- `docs/process/using-recall.md`, `docs/architecture/overview.md` — steps 8 and 9, plus the two
  D12 repairs `impl-report.md` declares as deviation 3.
- **`recall/store.py` is not in the diff**, which is the plan's claim that a deletion needs no new
  persistence machinery, standing up.

No hunk serves neither a criterion nor a plan step. No unrequested scope.

## Findings

**F1 — a false claim in `docs/architecture/overview.md`, repaired here (D12).** The `store.py`
bullet read: *"Keeping it silent is what lets the same load path serve `add`, `list` and, later,
`review` without each of them re-deriving what a corrupt file means."* It was written when
`review` was unbuilt; `WI-0003`'s review recorded it as a known-stale sentence carried forward,
outside that item's D12 scope. This item put it inside scope, because `cmd_delete` is a **fourth**
caller of that load path. Repaired in place — it now names all four subcommands and cites
`recall/cli.py` — with the file bumped to **v7** and a change-log row saying what was wrong. The
decision it describes is untouched, so nothing is superseded. Repaired rather than sent back
because the sentence is documentation, the correction is one clause, and the project has the same
precedent at `using-recall.md` v2, where a review corrected a citation in place.

**F2 — three prose lines over the width the rest of both files keep.** `using-recall.md` v6 left
two lines at 160 and 115 characters and `overview.md` v6 one at 111, where every other non-table
line in both files is ≤ 100. Cosmetic, no claim affected; re-wrapped in the same v7 bumps, with a
change-log row stating that no claim changed.

**F3 — `verify-report.md`'s `Verified-commit:` line did not parse, and only this skill's gate
could tell.** The line read `Verified-commit: <sha> (branch \`wi/WI-0004\`)`. `check-verify-freshness`
matches the sha to end of line, so the parenthetical made it report *"verify-report.md has no
'Verified-commit: <sha>' line"* — the same message it gives for a report that names nothing at
all. The sha was correct and the verification was genuinely current, so this is a formatting
defect, not a stale verification: repaired here by moving the branch name onto its own line,
with a note in the report saying what changed and that the sha did not. **This is a toolkit
observation as much as an item finding:** `verify` prescribes the line and commits its report, but
no gate `verify` runs parses it, so a malformed line survives until the next skill — where the
failure mode reads as "D10 failed" rather than "the line is misformatted". Worth a change to the
`verify` contract, and recorded here because this item is where it was found.

**No finding of substance against the change itself.** The implementation matches the plan, the
plan matches the criteria, and the criteria match the two answers the stakeholder gave.

## Accepted gaps

Each is recorded in `item.md`'s `## Notes` as well, so it survives this item being closed:

1. **`recall delete` inherits BUG-0001.** With the deck path existing as a directory,
   `recall delete --question "x"` exits 1 with an `IsADirectoryError` traceback — verification
   reproduced it. AC8 is not violated: AC8 governs a file that cannot be read *as a deck*
   (`DeckUnreadable`), and that path refuses correctly with exit 3. BUG-0001 already describes the
   class — *"`recall/cli.py` catches `store.DeckUnreadable` and nothing else"* — so no new bug is
   filed; what is new is that the fix now has **four** subcommands to cover.
2. **Concurrency is unverified.** Two deletions racing over one deck file is specified nowhere and
   nothing exercises it. `ADR-0004`'s atomic rename bounds the damage to "one write wins", which
   is an argument rather than a measurement. Accepted: single-person tool, no criterion asks.
3. **Exact matching will be unhelpful before it is wrong.** A question typed with an invisible
   trailing space gets "no card has that question" and no hint. The mitigation shipped — the
   refusal quotes back what was typed and says to type it as `recall list` shows it — and
   anything better is a product decision. `plan.md`'s risk list and the item's `## Notes` both
   already carry it; repeated here because it is the most likely source of a future complaint.
4. **AC7's tab case is delivered through shell quoting**, not through an interactive terminal
   where readline may intercept a tab. That is a property of terminals, not of `recall`.

## Verdict

**Accepted and closed as `delivered`.** All twelve criteria are ticked with evidence a reader can
re-run; the Definition of Done passes on all twelve points, D12 after one repair; the trial merge
of `wi/WI-0004` into `main` produced `04c5a38` and the suite passed on that merge result (55
tests, OK) with `compileall` clean; `main` was confirmed unmoved at `152c531` after the trial
worktree was removed. Three findings, all repaired in this review and none requiring a send-back.
Four gaps accepted and written into the item's `## Notes`.

The engagement is **not** over: `engagement-state EP-001` reports `active`, with BUG-0001 still in
flight. No sign-off is filed and none is due yet.
