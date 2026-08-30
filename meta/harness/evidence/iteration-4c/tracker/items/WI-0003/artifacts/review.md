# Review — WI-0003

## What I examined

- `item.md` — the nine acceptance criteria, all nine ticked, and the `## Out of scope` and
  `## Notes` sections that record what the stakeholder decided and what was assumed under their
  standing deferral.
- `history.md` — eight rows, `— → draft → awaiting-answer → draft → ready → planned →
  in-progress → verifying → in-review`, chaining without a gap and ending at the status
  `item.md` carries.
- `journal.md` — read in full, all eight entries: `answer-questions` (creation), `refine`
  (suspended with two questions), `answer-questions` (both answers propagated), `refine` (the
  Definition of Ready pass), `plan`, `implement` twice, `verify`.
- `questions/Q-001.md` and `questions/Q-002.md` — both `answered` by the human, both with
  `## Consequences` naming files that exist: `ADR-0005`, and this item's AC1, AC2, AC6 and
  `## Out of scope`.
- `artifacts/plan.md` — nine steps, the criteria mapping, four reversible assumptions with their
  reversal costs, and the decisions table.
- `artifacts/impl-report.md` and `artifacts/verify-report.md` — including `## What I did not do`
  and `## Not verified, and why`, judged one by one in `## Accepted gaps`.
- **The diff itself**, `git diff main...wi/WI-0003`, hunk by hunk — not the reports about it. Four
  code hunks in `recall/cli.py`, one new file `tests/test_delete.py` read in full, and the tracker
  files.
- `docs/architecture/adr/ADR-0005-…` — read clause by clause against `recall/cli.py`, which is
  where the erratum below came from.
- `docs/architecture/overview.md` v4 and `docs/product/vision.md` v6 — the D12 read.

**The D12 claims audit, claim by claim.** Each was decided by opening what it cites, not by
reading the sentence:

| claim | what I opened | verdict |
|-------|---------------|---------|
| `overview.md` line 12 — *"`add` and `review` built and merged, and `delete` not yet started"* `[src: WI-0003]` | `tracker/items/WI-0003/item.md`, and the branch | **false at the merge** — repaired, v5 |
| `overview.md` §How it is run — *"`delete` is named here so a reader can see where it will attach"* `[src: WI-0003]` | the same | **false at the merge** — repaired, v5 |
| `overview.md` §The pieces — the store *"reads it into cards, appends or removes, and writes it back atomically"* `[src: recall/store.py]` | `recall/store.py` in full | **false** — the module offers `load` and `save` and no other public operation; `cards.append(...)` is in `cli.add` and `del cards[chosen]` is in `cli.delete`. Wrong since v1, when only `add` existed. Repaired, v5 |
| `overview.md` §How it is run — *"Confirmations go to standard output; warnings and refusals go to standard error"* | `recall/cli.py`'s `delete`, `_confirmed`, `main` | **true** — `Deleted:` and `Nothing was deleted.` are stdout at exit 0; the no-match refusal and the parse refusal are stderr at exit 1 |
| `overview.md` §How it is checked — *"No test run touches a real deck"* `[src: tests/test_review.py]` | `tests/test_delete.py`'s `environment()` | **true**, and now says why: `RECALL_CARD_FILE` is set into a temporary directory and `XDG_DATA_HOME` is popped from the child's environment. Citation for `test_delete.py` added, v5 |
| `overview.md` §What the card file looks like — the format, and *"every save rewrites the whole file through a temporary file and a rename"* `[src: ADR-0008]` | `recall/store.py`'s `save`, and the file `delete` left behind | **true** — deleting the last card leaves the two header lines and a file `review` and `add` both still read |
| `ADR-0005` §Decision — named by front side *"typed exactly as it was entered"*, no listing, no number | `recall/cli.py`'s `delete`: `card.front == front` | **true** — exact equality, no strip, no case fold |
| `ADR-0005` §Decision — the card *"and the date it is next due"* shown, removed *"only on an affirmative reply"*; a negative reply *"an ordinary outcome, not an error"* | `_described`, `_confirmed`, and the runs in `verify-report.md` | **true** |
| `ADR-0005` §Decision — a no-match *"exits non-zero and leaves the stored file unchanged"*; several matches listed and *"exactly the chosen one is removed"* | `delete`'s three paths, and the interleaved-match run | **true** |
| `ADR-0005` §Consequences — *"The item declares no `depends-on` and passes Definition of Ready R7 in form"* `[src: WI-0003]` | `tracker/items/WI-0003/item.md`'s front matter | **false** — it declares `depends-on: WI-0001`. Repaired as an `erratum`, v2 |
| `vision.md` §Throw a card away — deleted *"named by its front side"*, the tool shows *"the ladder it had reached, when it was next due"* and removes *"only when they say yes"*; *"Deleting is permanent"* | `recall/cli.py`, and the AC2 prompt output | **true** in every clause |

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | nine `- [x] AC` lines in `item.md`, zero `- [ ] AC` |
| D2 | every ticked criterion cites its evidence | **pass** | `verify-report.md` `## Criteria` has a row per AC naming the command and quoting its real output; the implementation report is cited as evidence nowhere in it |
| D3 | the gates passed on the **final** state of the code | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 90 tests` / `OK` and `python3 -m compileall -q recall tests` → exit 0, both re-run by this review on the **merge result** in a detached worktree, not on the branch alone |
| D4 | no open blocking question | **pass** | `Q-001` and `Q-002` are both `status: answered`, `answered-by: human`, with `## Consequences` naming files that exist |
| D5 | a journal entry per execution, history chains | **pass** | eight history rows, eight journal entries, timestamps in the same order; the last row's `to` is `in-review`, which is `item.md`'s status |
| D6 | design decisions are in ADRs, cited from the plan or journal | **pass** | `plan.md`'s decisions table cites `ADR-0005`, `ADR-0007`, `ADR-0008`, `ADR-0002`, `ADR-0006` and states why **no new ADR** was written — every decision this change forces was already recorded or is one of four reversible assumptions listed in the plan. Reading the diff against `ADR-0005` clause by clause found no contradiction |
| D7 | documents the change invalidated are updated, with a version bump and a change-log row | **pass** | `overview.md` v4 → **v5** (three false sentences repaired, change-log row written) and `ADR-0005` v1 → **v2** (one `erratum` in the append-only `## Corrections` section, with the removed text quoted verbatim and a matching change-log row). Committed at `677aac3` |
| D8 | every commit on the branch references the item | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → `all 4 commit(s) on main..wi/WI-0003 name WI-0003`, exit 0 |
| D9 | merged into the trunk | **pass** | merged after this record was written and the item closed — the order step 8 requires, because `check-commit-refs` reads `main..branch` and that range is empty once merged |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0003 wi/WI-0003` → *"verified at 1ebf08ef; wi/WI-0003 has moved to 677aac33 but only the record changed (7 file(s) under tracker/ or docs/), so the verification still covers the code"*, exit 0. The last change to `recall/` or `tests/` is `fe70136`, which predates the verification |
| D11 | `review.md` exists and says what was examined | **pass** | this file, `## What I examined` first |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass, after two repairs** | the eleven-row table in `## What I examined`. Three sentences were false and are repaired; eight were read against what they cite and are true. `lint-claims --context work-item --changed-since main` was run **twice**: before the repairs it reported *"0 document(s) in 0 path(s) differ from main"* — a green over nothing — and after them *"2 document(s) in 2 path(s)"*, 0 errors, which is a green over something |

## Findings

1. **`recall/store.py` never appended and never removed.** `overview.md` had said, since v1, that
   the store *"reads it into cards, appends or removes, and writes it back atomically"*, citing
   `recall/store.py`. Opening the module shows `card_file_path`, `load` and `save` and no third
   public operation; `cards.append(...)` lives in `cli.add` and `del cards[chosen]` in
   `cli.delete`. The sentence describes a seam one module to the left of where it is. It matters
   because the next skill to add a subcommand would look in the wrong module for the operation it
   needs — which is precisely what `plan.md`'s assumption 1 had to reason about from the code
   instead of from the document. **Repaired**, not sent back: `implement` and `verify` are both
   forbidden to write to `docs/` (`spec/doc-header.md` §5), the item's own criteria say nothing
   about the overview, and D7 makes the repair this skill's.
2. **`ADR-0005` described a dependency the item no longer lacked.** Its `## Consequences` said
   *"The item declares no `depends-on` and passes Definition of Ready R7 in form"*. The second
   `refine` execution added `depends-on: WI-0001`, and nothing went back to the ADR. **Repaired
   in place** as an `erratum` through the append-only `## Corrections` section
   (`spec/doc-header.md` §4b): the removed clause is quoted verbatim, the replacement cites the
   item and its history, and nothing in `## Decision` moves — no reader would have to change any
   code to satisfy the new sentence, which is the line between a correction and a supersession.
3. **The two halves of AC9 name `delete` differently, and both pass.** `delete` with no argument
   prints the subparser's own usage, `usage: recall delete [-h] front`. `delete a b` prints the
   top-level usage, where `delete` appears inside `{add,review,delete}` and the error names the
   surplus argument rather than the subcommand. `verify` recorded the difference rather than
   smoothing it, which is the right call: the criterion asks for a usage message naming the
   `delete` subcommand and both messages contain it. Not a defect and not a send-back —
   tightening it would be a change to AC9. Recorded here so it is not rediscovered as news.
4. **Every hunk of the diff maps to a plan step and a criterion.** `_rung` and `_described` →
   step 2, AC2 and AC6. `delete`'s no-match branch → step 3, AC5. `_confirmed` → step 4, AC2 and
   AC7. `_chosen_among` → step 5, AC6 and AC7. The `delete` subparser → step 6, AC9. The `main()`
   rewrite → step 6. `tests/test_delete.py` → step 7. **No unrequested scope.** `review()`,
   `_stopped()`, `_ask()`, `add()` and `_side_error()` are byte-identical to `main`, and
   `recall/schedule.py` and `recall/store.py` are not in the diff at all.
5. **The one hunk that serves no criterion is defensible and I would keep it.** `main()`'s closing
   `raise AssertionError("no handler for subcommand …")` is unreachable, because argparse's
   `required=True` refuses an unregistered subcommand first. It exists so that a *fourth*
   subparser added without a handler fails loudly instead of falling through to whichever branch
   the chain ended with — the trap `WI-0001`'s own review recorded and `WI-0002` had to disarm.
   Plan step 6 accounts for it. Being unreachable it is untested, and that is the correct state
   for a guard of this kind; the alternative is a test that reaches into the parser to break it.
6. **No defect belonging to another item.** Nothing was found that `WI-0001` or `WI-0002`
   delivered and got wrong, so no bug item was filed.

## Accepted gaps

Each is recorded in the item's `## Notes` as well as here, because nobody reads a verification
report after an item closes.

1. **The card file's default location was never exercised by `delete`.** Every test and every
   verification run set `RECALL_CARD_FILE`. `delete` calls the same `store.card_file_path()` as
   `add` and `review`, which `tests/test_store.py` covers directly and which this branch does not
   touch. Accepted: writing to a real `$HOME` from a test run is the thing the convention exists
   to prevent.
2. **The concurrent-writer gap.** `delete` reads the file, waits at a prompt indefinitely, then
   writes back the list it read; a second `recall` process writing in between would be lost.
   `ADR-0008`'s atomic rename means the loser is overwritten rather than the file corrupted.
   Accepted — it is the whole tool's gap, already accepted at `WI-0002`'s close, and it belongs to
   `recall/store.py` for every subcommand at once if it is ever addressed. Not a new liability
   from this item.
3. **No unicode-normalisation case.** Matching is exact equality, so a front differing only by
   case, by surrounding whitespace or by normalisation form does not match.
   `NoMatchTests.test_a_near_miss_is_not_a_match` covers case and whitespace; no composed/decomposed
   pair was constructed. Accepted: this is `plan.md`'s assumption 2, taken deliberately because
   `ADR-0007` stores a side verbatim and anything looser would delete a card the person did not
   type.
4. **`Ctrl-D` was never pressed at a real terminal**, at either prompt; a closed pipe stands in for
   it. Accepted — it is the same evidence `WI-0002` AC11 rests on.
5. **The prompt does not wrap**, so a long side runs past a narrow terminal's edge. No criterion
   constrains the width. Accepted; if it ever matters it is a new item, not a defect against these
   criteria.
6. **AC4's "survives stopping and starting" is separate subprocess invocations**, not a reboot.
   Accepted — the same limit `WI-0001` recorded for its AC2, and the stronger reading is not
   testable in this project.

## Verdict

**Accepted and closed, `outcome: delivered`.**

The change does what WI-0003 asked for, in the module that already held the other two
subcommands, without touching `review`, the ladder or the stored format. Verification was
independent and had teeth: nine criteria each settled by a command, nine mutations each turning
the suite red, and the one hazard the plan named — a non-matching card sitting between the
matches — exercised explicitly.

Two documentation defects were found by reading rather than by a gate, and both are repaired
here rather than deferred. The second of them, `overview.md`'s claim that the store appends and
removes, had survived four versions and three items precisely because it *looked* checked: it
carried a resolving citation, and `lint-claims` proves that a citation resolves, never that it
supports the sentence.
