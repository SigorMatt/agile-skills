# Review — BUG-0001

## What I examined

- **The item.** `tracker/items/BUG-0001/item.md` — the summary, the reproduction, the expected and
  actual behaviour, the four acceptance criteria and their tick state, and the five notes the
  filing skill left.
- **The record.** `history.md` in full — five rows, chaining `— → ready → planned → in-progress →
  verifying → in-review`, the last row agreeing with the item's status. `journal.md` in full —
  five entries, one per execution the history implies: `verify` filing the bug, `plan`, `implement`
  twice (the branch, then the completion), and `verify` again. No question was ever filed on this
  item and its `questions/` directory is empty.
- **The design.** `artifacts/plan.md` — eight steps, four criteria mapped, three assumptions, and
  an out-of-scope list. `docs/architecture/adr/ADR-0009-a-documents-own-bug-is-fixed-by-the-item-that-owns-it.md`
  in full, including its options A to D and the reasoning that lets `implement` write to
  `docs/product/vision.md` for this item.
- **The change itself, hunk by hunk.** `git diff main -- docs/product/vision.md`: three hunks,
  9 insertions, 8 deletions. Hunk 1 is the front matter (plan step 3). Hunk 2 is the two
  paragraphs, each gaining one citation at the end of the sentence carrying its absolute (plan
  steps 1 and 2), with three lines of the first paragraph rewrapped. Hunk 3 is the new
  change-log row (plan step 3). `git diff --name-only main..HEAD` shows one file outside this
  item's own tracker directory. Nothing under `expenses/`, `tests/` or `README.md` is touched
  [src: tracker/items/BUG-0001/artifacts/plan.md].
- **The reports.** `artifacts/impl-report.md`, including its declared deviation, and
  `artifacts/verify-report.md`, including `## Not verified, and why` and the three injections the
  verifier ran.
- **The claims, from what they cite — D12.** Both absolute claims this item touched were decided
  here by opening the cited things, not by reading the sentence:
  - *"The product deliberately has no per-person amounts and no weights."* Cites `WI-0001/Q-001`
    and `expenses/store.py`. The stakeholder's verbatim answer in that question refuses per-person
    amounts and weights in as many words, and records that they understood an uneven bill becomes
    two entries. `add_expense` at `expenses/store.py:109` takes an amount, a payer, a list of
    sharers, a date and a description; it derives `shares_minor` from `split_equally` over the
    sharers, and neither a weight nor a per-person amount appears in its signature or in the
    record it appends [src: expenses/store.py]. The sentence is true and its citation supports it.
  - *"It cannot be edited in place."* Cites `WI-0001/Q-003` and `expenses/cli.py`. That answer
    records editing as refused when the stakeholder was made to choose, and says a correction is a
    delete and a re-record. `grep -n edit expenses/cli.py` returns nothing at all — the parser
    registers `add`, `list` and `delete` under each of `person` and `expense`, and there is no
    `edit` subcommand anywhere in the file [src: expenses/cli.py]. True, and supported.
- **Gate runs of my own**, listed in the table below, plus a trial merge of `wi/BUG-0001` into a
  throwaway worktree of `main` with the suite run on the merge result.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `item.md` lines 82, 84, 88, 90 — AC1 to AC4 all `[x]` |
| D2 | every ticked criterion cites its evidence in the verification report | **pass** | `verify-report.md` `## Criteria` gives each AC its own row naming the command run and quoting its output; no row cites `impl-report.md`. AC1's row names three separate runs, AC2's names the diff and the read-back, AC3's names the two `sed` reads, AC4's names the validator |
| D3 | the declared gates passed on the final state, not an earlier one | **pass** | I re-ran them here on `129ffb9`, the current head: the suite → exit 0, `Ran 123 tests`, `OK`; `lint-claims --changed-since main` → exit 0, 1 document, 0 errors; `validate-workspace .` → exit 0, 7 items, 11 documents, 0 errors; `check-commit-refs` → exit 0. `lint-clean` is skipped project-wide (ADR-0004) and is recorded as skipped, not passed |
| D4 | no open blocking question | **pass** | `tracker/items/BUG-0001/questions/` is empty; none was ever filed, which both journal entries that could have filed one record explicitly |
| D5 | a journal entry per execution, history chaining to the current status | **pass** | five history rows and five journal entries, matched one to one by timestamp: `00:12:31` verify, `02:16:21` plan, `02:16:58` implement, `02:19:28` implement, `02:24:18` verify. The last row reads `verifying → in-review` and `item.md` says `in-review` |
| D6 | every design decision in an ADR, cited from the plan or journal | **pass** | the one design decision this item needed — which skill may edit a document that is itself the defect — is ADR-0009, written by `plan` before implementation began. `plan.md`'s `## Decisions and ADRs` table cites it in three rows, and `impl-report.md` cites it for `updated-by: implement`. The three reversible choices below that line are recorded as assumptions, which is the right place for them |
| D7 | documents the change invalidated updated, with a version bump and a change-log row | **pass** | `docs/product/vision.md` is the document, and it went to `version: 4` with a matching top change-log row naming the timestamp, `implement`, and `BUG-0001`. `docs/architecture/overview.md` is deliberately untouched: this item alters nothing about the shape of the system, and the plan says so |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs BUG-0001 wi/BUG-0001` → `all 3 commit(s) on main..wi/BUG-0001 name BUG-0001`, exit 0 |
| D9 | merged into the trunk | **pass** | merged after this review was written and the item closed, in the order the procedure requires — see `## Verdict` |
| D10 | verification ran after the last code change | **pass** | `check-verify-freshness BUG-0001 wi/BUG-0001` → exit 0. I did not stop at the script: `git diff --name-only 76e62a6..HEAD` lists five files, every one under `tracker/`, and `git diff --name-only 76e62a6..HEAD -- docs/` is empty. So nothing this item delivers moved after `76e62a6`, which is the commit `verify-report.md` names. The check mattered here more than usual, for the reason in `## Findings` |
| D11 | the review record states what was examined | **pass** | this file, `## What I examined` |
| D12 | claims in `docs/` about the touched behaviour still true; absolute claims this execution wrote carry a resolvable citation | **pass** | the two claims were audited above by opening what they cite, not by re-reading them. The automated half: `lint-claims --changed-since main` → exit 0, and the whole-tree form `lint-claims --all` → exit 0, 0 errors, 0 warnings, run here on the current head with every artifact of this item present |

## Findings

1. **`check-verify-freshness` counts `docs/` as record, which makes D10 weaker for a
   document-only item than for a code one.** The script's own message here reads *"only the record
   changed (5 file(s) under `tracker/` or `docs/`), so the verification still covers the code"*.
   For every other item in this project that reasoning is sound, because the deliverable is under
   `expenses/`. For BUG-0001 the deliverable *is* a file under `docs/`, so an edit to
   `docs/product/vision.md` made after verification ran would have been classified as a record
   change and D10 would have passed over it. It did not happen — I checked the range directly and
   no file under `docs/` moved after the verified commit — so this is not a defect in the change
   and the item is not sent back. It is a property of the toolkit rather than of this project,
   and it belongs in the same place as the item's other toolkit observations: nothing in
   `tracker/` or `expenses/` can fix it, so no bug item is filed here.
2. **The declared deviation from plan step 1 is acceptable.** The step says to change no other
   word of the paragraph; three of its lines were rewrapped because the added citation pushed a
   line past this document's width. The diff's three removed lines and three added lines carry the
   same words in the same order, and AC2 is about what the paragraph says. `implement` recorded
   it rather than leaving it to be discovered, which is the behaviour the deviation section exists
   for.
3. **No unrequested scope.** Every hunk maps to a plan step: hunk 1 and hunk 3 to step 3, hunk 2 to
   steps 1 and 2. The other absolute claims in `vision.md` were left alone exactly as the plan's
   out-of-scope list requires, which is the easy over-delivery this item invited and did not take.
4. **Nothing contradicts an ADR.** The one departure a reader might flag — `updated-by: implement`
   on the product vision, against the writer table in `spec/doc-header.md` — is the subject of
   ADR-0009 and is what that ADR decided. The change does what the ADR says.

## Accepted gaps

Copied into the item's `## Notes` as well, because a report stops being read once an item is
`done`.

- **`lint-clean` never ran, on any execution of this item.** `tracker/project.yaml` records
  `lint: null`, ADR-0004 is the decision behind it, and every skill recorded the gate as skipped
  rather than passed. For an item that adds no code this leaves nothing meaningful unchecked.
- **The other absolute claims in `vision.md` are still unsourced.** "no accounts, no sync, no
  sharing of the dataset" and "No network access, no hosted service, no bank connection" name
  nothing as code or as a path, so the rule in `spec/doc-header.md` §4a does not reach them and
  the linter does not flag them. Accepted, not deferred: there is no defect here to fix, and
  sourcing them would be a change no criterion asks for.
- **The scoping that let this defect past three contracted gates is unchanged.** Every skill's
  `claims-are-sourced` gate reads only what changed since the trunk, which is why `plan`,
  `implement` and `review-close` all ran clean over `vision.md` while the whole-tree form failed.
  Both the plan and the verification report put it out of scope, and it is out of this project's
  reach: the gate definitions live in the toolkit. What survives this item is the practice —
  `lint-claims --all` finds document defects that the contracted gate cannot, and it is worth
  running by hand.
- **Finding 1 above**, the freshness script's treatment of `docs/`, on the same footing and for
  the same reason.

## Verdict

**Accept.** All twelve Definition of Done criteria pass, each with its own evidence above. The
change does what BUG-0001 asked and nothing else: two citations, a version bump, a change-log row,
one file.

The trial merge was made first, into a throwaway worktree of `main`, and the suite was run on the
merge result: `Ran 123 tests in 1.526s`, `OK`, exit 0. The merge was a fast-forward, so the merge
result is the branch head commit-for-commit and the whole-tree claims linter run on that head
applies to it unchanged. The trial worktree was then removed and `git worktree list` showed only
the project.

The item is closed `done` with `outcome: delivered` while the branch is still unmerged — because
`check-commit-refs` reads `main..wi/BUG-0001`, and merging first would empty that range and make
the gate refuse the close it is a precondition for. The real merge follows the close.
