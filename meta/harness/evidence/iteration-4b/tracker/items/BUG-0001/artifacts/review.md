# Review — BUG-0001

## What I examined

- **The diff, hunk by hunk**, over `ec112a4..c9a85a0` (`main..wi/BUG-0001`): `recall/store.py`
  (+160/−63 across the branch), `recall/cli.py` (+68), `tests/test_deck_file_errors.py` (+236,
  new), `docs/architecture/overview.md` (v8→v9) and `docs/process/using-recall.md` (v7→v9). Each
  hunk was mapped to a plan step or a criterion; the mapping is under `## Findings`.
- **The record**: `item.md`, all six rows of `history.md`, all eight entries of `journal.md`,
  `plan.md`, `impl-report.md`, `verify-report.md`, and the item's `questions/` directory (empty —
  no question was ever filed on this item).
- **`ADR-0010`** in full, against the code that claims to implement it — §1 (the exception
  family), §2 (`path` is always the deck file), §3 (the classifier's three branches, and its
  `## Consequences` clause that the classifier returns rather than raises), §4 (`FileNotFoundError`
  alone is absence), §5 (one exit code), §6 (where `cli` catches what).
- **`ADR-0004` §5 and §6**, because `load`'s narrowed catch touches the line they draw between
  absent and unreadable. §6 reads *"A missing file, and a missing parent directory, mean …"* — the
  narrowing implements it and does not supersede it.
- **The claims audit (D12), from the citations rather than from the prose.** Each absolute claim
  the item touched, and the thing I opened to decide it:

  | claim | cited | what I opened, and the verdict |
  |---|---|---|
  | `overview.md`: *"Only the first is a normal state, and only `FileNotFoundError` produces it"* | `recall/store.py`; `ADR-0004` | `store.load` — `except FileNotFoundError: return Deck()` is the only path returning an empty deck; the following `except OSError` raises. **True** |
  | `overview.md`: *"`cli` reads no `errno` and no exception filename and never learns that a write goes through a temporary file"* | `ADR-0010`; `recall/store.py` | `grep -n "errno\|\.filename" recall/cli.py` → no match outside the module docstring's own sentence. **True** |
  | `using-recall.md`: *"Every subcommand names the deck file, says whether it could not be **read** or could not be **written**, writes nothing, and exits non-zero"* | `BUG-0001` AC1, AC2; `ADR-0010` | ran all four subcommands under reproduction B: `list`, `add`, `review` and `delete` each exit `3` with `cannot read the deck file …/deck.json -- it is a directory, not a file. …`. **True** — and it is the sentence this execution's v9 edit repaired, since a deck folder at mode `000` used to traceback |
  | `using-recall.md`: *"the message names *that* instead, because that is the thing you have to move"* | `BUG-0001` AC3 | reproduction C and the `$HOME`-is-a-file probe: both name the obstructing ancestor, not the deck. **True** |
  | `using-recall.md`: *"only a missing file, or a missing folder on the way to it, counts as 'no deck yet'"* | `ADR-0004`; `ADR-0010` | `ADR-0004` §6 and `store.load`'s narrowed catch — the two agree, and `NotADirectoryError` no longer reaches the absent path. **True** |
- **The declared gaps**: `## Not verified, and why` in the verification report (six items) and
  `## What I did not do` in the implementation report (five). Each is decided under
  `## Accepted gaps`.
- **A trial merge and its test run**, and `main`'s sha either side of it.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | AC1–AC6 all `- [x]` in `item.md`; `validate-workspace` → 0 errors |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | its `## Criteria` table gives a command and quoted output per criterion, all measured at `bb74d04`; `impl-report.md` is cited as evidence for none of them |
| D3 | gates passed on the final state of the code | **pass** | the last code commit is `5bf6141`; `implement`'s gates ran at that head and `verify`'s at `bb74d04`, which differs from it only under `tracker/`. The two later commits are record-only |
| D4 | no open blocking question | **pass** | `tracker/items/BUG-0001/questions/` is empty; no question was ever filed on this item |
| D5 | a journal entry per execution, history chains without a gap | **pass** | six history rows, eight journal entries — the two extra are the filing entry (`verify`, 02:08) and the reproduction-C addition (`review-close`, 02:13), both from WI-0001's review, before the item had a status of its own to move. `validate-workspace` accepts the chain |
| D6 | every design decision is in an ADR, cited from the plan or journal | **pass** | `ADR-0010` records the whole design and is cited in `plan.md` and in four journal entries. The second execution's `os.path.isdir` choice is *not* a new decision: `ADR-0010` §3 already specifies the classifier's branches and its `## Consequences` already requires it not to raise, so the change restores the recorded design rather than altering it — the reasoning is in the developer's journal under `**Decisions:**` |
| D7 | invalidated documents updated, with a version bump and a change-log row | **pass** | `using-recall.md` v7→v8→v9 and `overview.md` v8→v9, each with a change-log row naming what changed and why. v9 of `using-recall.md` is the repair the second execution owed: the page's refusal list did not include a folder that cannot be read, which was the one case where its "exits non-zero" claim was false |
| D8 | every commit references the item ID | **pass** | `check-commit-refs BUG-0001 wi/BUG-0001` → `all 9 commit(s) on main..wi/BUG-0001 name BUG-0001`, exit 0 |
| D9 | merged into the trunk | **pass** | merged after this review was written and the item closed, in that order — see `## Verdict` |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness BUG-0001 wi/BUG-0001` → `verified at bb74d04a; wi/BUG-0001 has moved to c9a85a0b but only the record changed (5 file(s) under tracker/ or docs/)`, exit 0 |
| D11 | `review.md` exists and says what was examined | **pass** | this file; `## What I examined` is first and names the diff range, the artifacts, the ADRs and the claims audited |
| D12 | claims in `docs/` about the touched behaviour are still true; absolute claims carry a resolvable citation | **pass** | the five-row table above, each decided by opening what the sentence cites; `lint-claims --context bug --changed-since main` → `2 document(s) in 2 path(s)`, 0 errors. The scope contained the two documents this item changed, so the gate could have found something |

## Findings

**Every hunk traces to a plan step or a criterion.** The mapping, in the diff's order:
`store.py`'s exception family → steps 1 and `ADR-0010` §1; `_obstruction` → step 2; `_refusal` →
step 3 and §3; `load`'s narrowed catch and new `except OSError` → step 4 and §4; `save`'s wrapper →
step 5 and §2; `cli.py`'s four widened `except` clauses → step 6; the constant rename and the three
`store.save` guards with `_report_unwritable` → step 7 and §5; the test file → step 8 plus the
implementer's declared deviation 2; the two documents → steps 10 and 11. Nothing in the diff serves
neither. Nothing contradicts an ADR.

**F1 — a variable name that is now narrower than what it holds.** All four load-side handlers read
`except store.DeckError as unreadable`, and the binding can hold a `DeckInaccessible`. The message
`_report_unreadable` prints is right either way — both conditions arise on a read — but the name
says something that is no longer exactly true, and the next person to extend that handler will read
it. Not sent back: cosmetic, no behavioural consequence, and a send-back costs a full
implement-and-verify cycle. Recorded in `item.md` `## Notes`.

**F2 — one documentation example quotes less than the tool prints.** In `using-recall.md`, the
write-refusal block quotes the whole message; the obstruction block below it stops after the first
sentence, where the tool continues *"Nothing has been written and the file is exactly as it was.
Move it aside or repair it by hand, then run recall again."* Everything shown is real output, so no
claim is false — the two blocks are just inconsistent about completeness. Recorded, not sent back.

**F3 — a stale enumeration in a test module's docstring.** `tests/test_deck_file_errors.py` opens
by naming three conditions and saying *"the three reproductions here are BUG-0001's"*; the file now
holds four classes, the fourth being the mode-`000` directory the send-back added. That class
carries its own docstring explaining where it came from, so nothing is unexplained. It is a comment
in a test file rather than a claim under `docs/`, so D12 does not reach it. Verification recorded
the same thing as O2. Recorded, not sent back.

**No finding rises to a defect.** The item's own criteria all hold, verification is current, and
the merge result is green.

**On the send-back this item survived.** The first implementation passed 61 tests with a classifier
that raised while classifying; the first verification found it by probing one step beyond the
criteria, and refused to tick a single box even though all six passed at that commit. That is the
behaviour the pipeline wants, and it is worth naming here: the criteria did not catch this, the
boundary probe did.

## Accepted gaps

All five are written into `item.md` `## Notes`, so they survive this item's closing.

1. **A dangling symlink where the deck's directory belongs still reports an empty deck at exit 0.**
   Unchanged by this item and defensible under `ADR-0004` §6. A question about that ADR's wording,
   not a defect in this code. Accepted.
2. **No test drives a write that fails after the temporary file is opened** (`ENOSPC`, a refused
   `fsync`, a refused `os.replace`). The wrapper covers them by construction. Accepted: provoking a
   full filesystem is beyond this suite, and both the implementer and the verifier declared it.
3. **`_refusal`'s `strerror is None` fallback is unexercised.** Accepted; it is a fallback to a
   class name, and no condition reached produced an `OSError` without a `strerror`.
4. **Root and concurrency are untested.** Accepted; consistent with every other item in this epic,
   and the skips are explicit and print their reason.
5. **F1, F2 and F3 above.** Accepted as cosmetic.

## Verdict

**Accept.** All twelve Definition of Done criteria pass, each with its own evidence. The trial
merge was made in a detached worktree of `main` (`git worktree add --detach /tmp/trial main`,
`git -C /tmp/trial merge --no-ff wi/BUG-0001` → `68c05a9`), the suite ran **on the merge result** —
`Ran 63 tests`, `OK` — and `compileall` exited 0 there. The trial was discarded and `git rev-parse
main` returned `ec112a49737596438da4b5f8156341376bf1dceb`, the same sha it returned before it, so
the trunk did not move.

The item is closed with `outcome: delivered` **before** the real merge, because
`check-commit-refs` inspects `main..wi/BUG-0001` and that range empties the moment the branch is
merged.

The real merge followed the close: `git merge --no-ff wi/BUG-0001` on `main` → merge commit
`531d896`, with the suite re-run on `main` afterwards (`Ran 63 tests`, `OK`) and the workspace
validating at 0 errors, 0 warnings. `engagement-state EP-001` then reported **`at-rest`** — every
child stopped, no question open, no request open, rest reached at `2026-08-30T05:43:23Z` — which is
the ending EP-001 must now be taken through, by a separate dispatch of this skill on the epic.
