# Review — WI-0001

## What I examined

- `item.md` — all eleven criteria, their tick state, `## Out of scope` and the five `## Notes`
  blocks recording what was assumed and under whose licence.
- `history.md` — twelve rows, read for the chain rather than the content: `from` chains to `to`
  at every row, the first row's `from` is `—`, and the last row's `to` is `in-review`, which is
  `item.md`'s status.
- `journal.md` — all thirteen entries in full. Twelve rows and thirteen entries is not a defect:
  the entry at `22:23:39Z` accompanies no move and says so (`in-progress` — unchanged), which is
  the standalone form `spec/journal-and-history.md` §2.2 provides for.
- `plan.md` — the seven steps, the nine-row invalidation set, the three binding ADRs, the five
  assumptions, the `## Known gate exception`, and `## Risks`.
- `impl-report.md` — the eleven-row evidence table, the three declared deviations, the
  enumeration behind the quantified claim, and `## What I did not do`.
- `verify-report.md` — all eleven criterion rows, the ten ADR conformance rows, the nine
  invalidation rows, the twelve-mutation sensitivity table, `## Defects found` and
  `## Not verified, and why`.
- All six questions in the engagement: `WI-0001/Q-001`, `Q-002`, `Q-003` and `EP-001/Q-001`,
  `Q-002`, `Q-003`. Every one `answered`, each `## Consequences` naming files that exist.
- **The diff, hunk by hunk**: `git diff main..HEAD` — thirteen files, of which ten are new under
  `droll/` and `tests/` and three are document edits. Every source file read in full.
- All four ADRs, `docs/architecture/overview.md` and `docs/product/vision.md`.

### Round 2 — what the resuming execution examined

The review above was written at `d66d1b0` and suspended on `Q-004`. `answer-questions` amended
`ADR-0004` to v3 and returned the item to `in-review` at `971e974`. This execution read, on top
of everything above:

- `Q-004` in full, including its `## Answer`, `## Cross-answer check` and `## Consequences`.
- `ADR-0004` v3 in full — `## Decision` points 4, 4a and the renumbered 5, and the change-log row.
- `plan.md`'s amended `## Known gate exception`.
- **The diff since the suspension**, `git diff d66d1b0..971e974 --stat`: seven files, all under
  `tracker/` or `docs/`. **No file under `droll/` or `tests/` has changed since `c2fa284`**, so
  the hunk-by-hunk read above still describes the code being closed, and
  `check-verify-freshness` says so independently at the current head.
- **The full gate run ADR-0004 point 4 condition 1 requires**: `run-gate --skill review-close
  --item WI-0001 --all --resolving 'WI-0001:in-review->done'` → exit 1. Every verdict it produced
  is in this execution's journal entry; the four-condition check is in the verdict below.
- **A fresh trial merge**, because the branch had moved since the first one: `git worktree add
  --detach`, `merge --no-ff` → `1a5c62c`, `python3 -m unittest discover -s tests -t .` → exit 0
  over 27 tests, `python3 -m compileall -q droll tests` → exit 0, then `git worktree remove
  --force`. `git rev-parse main` returned `6788e555` before and after.

### The claims audit (D12)

Each row opens the thing the claim cites and says what would have contradicted it.

**Claim 1 — `docs/architecture/overview.md` `## Shape`:** *"Three of the six files under `droll/`
touch the outside world, and each touches one part of it: … `droll/roller.py` calls the random
number generator it was handed"*, cited `[src: droll/cli.py:15; droll/roller.py:24]`.

- **Opened:** the citation itself, and then all six files under `droll/` with
  `grep -nE 'import (random|sys)|random\.|sys\.|open\(|\.write\(|\.readline\(|\.flush\(' droll/*.py`.
- **Verdict: FALSE**, in the sub-clause rather than the count. The count is right — three files
  reach out, three do not. But `droll/cli.py:5` is `import random` and `droll/cli.py:15` is
  `def run(stdin, stdout, randint=random.randint) -> int:`, so `cli` names the real generator
  exactly as `roller` does, and *"each touches one part of it"* does not hold of it. The line that
  shows this is `droll/cli.py:15` — **the sentence's own citation**.
- **Falsifier:** a file the sentence calls clean that reaches out, or a file it assigns one part
  that reaches another. The grep ran over **all six** files and over all four shapes of contact —
  `random`, `sys`, `open(`, stream reads and writes — rather than over the two the sentence
  expects to be interesting, so it could have produced either. It produced the second.
- **Repaired here**, in place: `overview.md` v2 → v3 with a change-log row. This is a correction
  inside this item's own invalidation set at an item close, which is the one document edit this
  skill's contract permits. No code changed.

**Claim 2 — `docs/architecture/overview.md` `## Components`, the `Depends on` cell for
`droll/cli.py`:** *"all three above"*.

- **Opened:** the cell, and the same grep output beside `droll/roller.py`'s cell.
- **Verdict: FALSE by omission.** `droll/cli.py` imports `random` at line 5 and uses it at line 15;
  `roller`'s cell names `random` for the identical construct and `cli`'s does not. Two rows of one
  table answering the same question two ways is the shape that drifts.
- **Falsifier:** a `Depends on` cell omitting a real import. Checked by reading every import line
  in every module against its own row rather than by reading the rows for plausibility, which is
  how the inconsistency between two adjacent rows became visible at all.
- **Repaired here**, in the same v3 bump.

**Claim 3 — `ADR-0002` `## Consequences`:** *"`plan` created both as empty files"*, of
`droll/__init__.py` and `tests/__init__.py`.

- **Opened:** both files, as bytes — `wc -c` → `0`, `0`, and `repr()` → `b''`, `b''`.
- **Verdict: HOLDS.**
- **Falsifier:** one byte in either file. This is an absolute whose boundary is at zero bytes, so
  it was checked **at** the boundary: `wc -c` alone reads `0` for a file containing a blank line
  in some tools, and the `repr` rules out even whitespace. The counterexample was live rather than
  hypothetical — the tests needed three helpers and a package marker is where they would naturally
  have gone; they went to `tests/support.py` instead, which is `implement`'s declared deviation 1.

**Claim 4 — `docs/product/vision.md:67`, `## Engagement state`:** *"Three questions are open with
them, all filed at intake"*.

- **Not audited under D12, and deliberately.** `spec/dor-dod.md` D12 puts engagement-state
  sentences out of scope: *"no item audit is charged with one"*, because nothing an item does makes
  one true or false. It is false today — all three are `answered` — and DE4 at the ending owns it.
  It is the live `claims-are-sourced` failure this close is overridden past under ADR-0004 v3
  point 4; see the verdict below.

**Claim 5 — `ADR-0004` `## Decision` point 4a**, added to `docs/` after the round-1 audit and
load-bearing for this close: *"`review-close`'s runs `lint-claims --context work-item
--changed-since main`, with **no** `--plan-documents`"*, cited to the installed contract.

- **Opened:** both contracts, and not only the rows the sentence points at.
  `grep -n 'plan-documents' .claude/skills/review-close/references/contract.md` → **no match,
  exit 1**, over the whole file;
  `grep -n 'lint-claims' .claude/skills/implement/references/contract.md` → line 52,
  `lint-claims --changed-since {{trunk}} --plan-documents {{item.id}}`. The gate run this
  execution performed also prints its own resolved command:
  `lint-claims --context work-item --changed-since main --root …`, with no such flag.
- **Verdict: HOLDS**, and it is why the two gate failures on this item are one consequence rather
  than two collisions. The companion sentence — *"what puts `vision.md` in `review-close`'s
  window is that it differs from the trunk"* — is confirmed by the gate's own scope line,
  *"3 document(s) in 3 path(s) differ from main (6788e55) under docs"*, and by
  `git diff main..HEAD --name-only -- docs`, which returns exactly `ADR-0004`, `overview.md` and
  `vision.md`.
- **Falsifier:** the flag appearing anywhere in `review-close`'s contract — in another gate's
  row, in the inputs table, in the escalation prose. The grep ran over the **whole file** rather
  than over the `claims-are-sourced` row, so a mention in any of those places would have produced
  a hit and made the sentence false. It produced none.
- **Not repaired, because nothing is wrong.** Recorded because the override this execution
  performs rests on it, and a reviewer who takes an authorisation on trust has not reviewed it.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every checkbox settled | **pass** | Eleven `- [x]`, zero `- [ ]`, zero `- [~]`, counted off `item.md`. No criterion was settled by substitution, so no wording question is owed |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | `## Criteria` carries eleven rows, one per AC, each naming a command and quoting its actual output. Spot-checked against the report rather than counted: AC3's row quotes a six-value `uniq -c` histogram over 200 rolls, AC10's quotes three exit statuses |
| D3 | gates passed on the final state of the code | **pass** | `verify` ran its nine gates at `5dd1dc3`. The branch has since moved to `971e974` and now carries this review, `Q-004` and ADR-0004 v3, but every change is under `tracker/` or `docs/`; no file under `droll/` or `tests/` has changed since `c2fa284`. `check-verify-freshness` agrees at the current head |
| D4 | no open blocking question remains | **pass** | Round 1 failed this by its own act, filing `Q-004`. It is now `answered` — `answered-by: answer-questions`, `answered-at: 2026-09-11T22:58:23Z`, with `## Consequences` naming ADR-0004, `plan.md` and itself, all of which exist and carry the change. `grep -l 'status: open' tracker/items/*/questions/*.md` returns nothing, across the whole engagement rather than this item alone |
| D5 | a journal entry per execution; history chains | **pass** | Twelve rows chain without a gap and the last matches `item.md`; thirteen entries, the extra being the declared standalone at `22:23:39Z` |
| D6 | every design decision in an ADR, cited from plan or journal | **pass** | ADR-0001 (grammar), ADR-0002 (standard library only), ADR-0003 (one stream), ADR-0004 (the bounded override). `plan.md` `## Decisions and ADRs` cites the first three by number and `## Known gate exception` cites the fourth. The five things not in an ADR are in `## Assumptions` with a named way to reverse each |
| D7 | invalidation set confirmed | **pass** | See `## Invalidation set confirmation` — nine entries, all disposed; three `to-update` documents each updated with a version bump and a change-log row; three `owned-by-ending` rows left untouched, confirmed from the diff rather than asserted; and the completeness question answered by reading the two documents the set does not name |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, `all 10 commit(s) on main..wi/WI-0001 name WI-0001` |
| D9 | merged into the trunk | **pass** | The close must precede the merge, because `commits-reference-the-item` reads the commits not yet on the trunk and merging empties that range. Round 1's trial at `906c204` is stale — the branch has moved — so a **fresh** trial ran at the current head: `git worktree add --detach`, `merge --no-ff` → `1a5c62c`, `python3 -m unittest discover -s tests -t .` on the merge result → exit 0 over 27 tests, `python3 -m compileall -q droll tests` → exit 0, worktree removed. `git rev-parse main` returned `6788e555` before and after, so the trunk did not move. The real merge is made immediately after the closing transition; its sha is not in the journal entry, which could not name a commit that did not exist, but in `item.md`'s `merge-commit`, written by `scripts/record-merge` (`spec/journal-and-history.md` §2.2b) |
| D10 | verification postdates the code | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: *"verified at 5dd1dc3d; wi/WI-0001 has moved to ef8aaa6f but only the record changed"* |
| D11 | `review.md` exists and states what was examined; every accepted gap dispatchable | **pass** | This file. `## What I examined` precedes the verdict; `## Accepted gaps` carries one row per gap with an owner and a disposition the orchestrator reads |
| D12 | claims in `docs/` about the behaviour this item touched are still true | **pass, with two repairs** | The five rows above. Two claims were false and are repaired in `overview.md` v3; one holds at its boundary; one is engagement-state and out of scope by D12's own wording; and claim 5, added to `docs/` after round 1 and load-bearing for this close, holds against both installed contracts |
| D13 | the plan's `binding-adrs` list is complete | **pass, qualified** | The three ADRs that bind the change's content — ADR-0001, ADR-0002, ADR-0003 — are listed and each carries `verify`'s conformance verdict. ADR-0004 is engaged and is **not** in `## Binding ADRs`; `lint-documents` says so as a warning. It is not undeclared: the plan carries it in `## Known gate exception` and as row nine of the invalidation set, and `verify` recorded a verdict for it regardless. What it constrains is a transition rather than a line of code, which is why it landed in a different section. Recorded as a finding, not a failure |

## Invalidation set confirmation

| document | disposition | confirmed by |
|----------|-------------|--------------|
| `docs/product/vision.md` — `## Engagement state`, *"Three questions are open with them…"* | owned-by-ending | `git diff main..HEAD -- docs/product/vision.md` has three hunks — header, `## What it is for`, change log. None falls between lines 65 and 76. Left alone, as required |
| `docs/product/vision.md` — `## Engagement state`, *"Two work items exist, both at `draft`…"* | owned-by-ending | Same diff, same three hunks. Left alone |
| `docs/product/vision.md` — `## What it deliberately is not`, closing paragraph | owned-by-ending | Same diff: the paragraph appears only as unchanged context. Left alone |
| `docs/architecture/overview.md` — `## Components`, the five module paths; `## Conventions`, *"Started as a module"* | verified-still-true | Reopened by `verify` and again here. The five paths exist and each holds what its row says; no packaging metadata exists. **But the `Depends on` cell for `droll/cli.py` was wrong**, and that cell is inside this row's scope — see claim 2 above. The disposition was right about the paths and wrong about one cell; repaired here rather than sent back, because no code is affected and the correction is one cell |
| `docs/architecture/adr/ADR-0002-standard-library-only-including-the-tooling.md` — `## Consequences` | verified-still-true | Reopened at the byte level; claim 3 above. Holds |
| `docs/architecture/overview.md` — `## Shape`, the outside-world sentence | to-update | Updated: v1 → v2 by `implement`, with a change-log row. The **replacement** was then found false in its sub-clause and is repaired at v3 — claim 1 above |
| `docs/product/vision.md` — `## What it is for`, closing sentence | to-update | Updated: v3 → v4 by `answer-questions`, header bumped, change-log row present, and the sentence now carries `[src: WI-0001/Q-001; EP-001]` |
| `docs/architecture/overview.md` — `## Components`, *"`cli` knows about streams and not about the grammar"* | to-update | Covered by the same v2 bump and row; the replacement at `overview.md:45-47` matches `droll/cli.py:7` |
| `docs/architecture/adr/ADR-0004-…md` — the whole document | to-update | Updated: v1 → v2 → **v3** by `answer-questions`; header at `version: 3`, `updated: 2026-09-11T22:58:23Z`, and a change-log row for each of the three versions. The v3 amendment answering `Q-004` falls inside the same disposition and needed no new row. `impl-report.md`'s copy of this row is stale and says `verified-still-true … unchanged (v1)`; `plan.md`, which carries the authoritative disposition column, says `to-update`, and the document really was amended. Recorded as a finding |

**Did this change falsify a document the set does not name?** The set names
`docs/product/vision.md`, `docs/architecture/overview.md`, `ADR-0002` and `ADR-0004`. The workspace
holds two more: `ADR-0001` and `ADR-0003`. Both were read in full against the code.

- **ADR-0001** asserts the grammar and, in `## Consequences`, that *"The expression reader is a
  pattern match over three numbers rather than an arithmetic parser"*. `droll/expression.py:15` is
  one compiled pattern with three named groups and no evaluation step. Not falsified — implemented.
- **ADR-0003** asserts in `## Consequences` that *"AC4 and AC11 can be observed by capturing
  standard output alone, without redirecting or interleaving a second stream"*. Checked at the
  case that could have contradicted it — a rejection, the only line whose stream was ever in
  question: `printf '3x6\n' | python3 -m droll 2>err >out` put the message on stdout and left
  stderr at **0 bytes**. Not falsified.

Neither needed a row. The answer is *no*, and it is a claim against an enumerated set of six
documents, not a memory.

**Re-asked at the resume**, because the set is only as good as its enumeration and `docs/` had
been written to since. `find docs -name '*.md'` still returns six: `vision.md`, `overview.md`
and ADR-0001 to ADR-0004. Nothing under `docs/` was created since round 1, and the only one
edited was `ADR-0004`, which is row nine of the set. The enumeration the answer rests on is
unchanged, and so is the answer.

## Sections restated at the ending

`not an ending` — this is an item close. `lint-documents --rule engagement-state-is-restated
--item WI-0001 --context work-item` reports *NOT APPLICABLE*, and no `## Engagement state`
section was touched by this execution or by this item's branch.

## Findings

1. **`## Shape` and `## Components` in `overview.md` both mis-stated where `random` is reached,
   and one of them cited the line that proves it.** Claims 1 and 2 above. Repaired at v3 rather
   than sent back: the sentences were written by `implement` on this branch, but no acceptance
   criterion, no ADR and no line of code depends on them, and a send-back would cost a full
   `implement` and `verify` cycle to change one cell and one clause. **This is the finding worth
   carrying upstream:** `verify` reopened this same row and passed it, because it enumerated
   `from droll.<module>` imports — the project-internal ones — and `import random` is not one.
   The two-stage read is what caught it; a single reviewer running the same query twice would not
   have.
2. **`impl-report.md`'s `## Documents` table records `ADR-0004` as `verified-still-true …
   unchanged (v1)`.** Stale: `answer-questions` later amended the ADR to v2 and moved the row in
   `plan.md` to `to-update`. `plan.md` is authoritative and is correct, and the document really
   was updated, so the substance is sound and only the report's copy is stale. Not a send-back —
   an implementation report is a report of an execution, not a live document, and nothing reads
   it as one.
3. **ADR-0004 is engaged but is not in the plan's `## Binding ADRs`.** D13 above. Declared in two
   other sections of the same plan and carrying a `verify` verdict, so nothing is hidden; the list
   would read better with it in it.
4. **`BUG-0001` was filed by `verify` during this item's verification** — a stray tracked file at
   the repository root — and is on the board at `ready`. Read and agreed: it is not this item's
   behaviour and the routing is right.
5. **The diff carries nothing unrequested.** Ten new source and test files, each traceable to a
   plan step; three document edits, each traceable to an invalidation row. `tests/support.py` is
   the one file the plan did not name and `implement` declared it as deviation 1; it holds three
   helpers, no test, and is the reason ADR-0002's empty-package-marker claim survived. Accepted.

## Accepted gaps

| gap | owner | disposition |
|-----|-------|-------------|
| `docs/product/vision.md:67`, the unsourced absolute in `## Engagement state`, which no skill may repair before the ending and which `claims-are-sourced` fails on at **this** close as it did at `implement`'s transition. ADR-0004 authorised one override, and authorised it for `implement`'s `in-progress → verifying` move only. **Resolved:** the question is answered and ADR-0004 v3 point 4 authorises a second bounded override for this transition. The sentence itself is still nobody's to repair before the ending, and is still row one of the invalidation set, disposed `owned-by-ending` | `answer-questions` | `question-filed:WI-0001/Q-004` |
| `verify`'s `## Not verified, and why`: no test drives a real terminal, so every observation reads a pipe and the tty ordering rests on ADR-0003 plus the flush after every write. Closing it needs a pty harness, which no criterion asks for and which ADR-0003's one-stream decision makes unnecessary for the criteria as written | none | `no-owner` |
| `verify`'s `## Not verified, and why`: `lint-clean` is a compile check, so unused imports, undefined names on unexecuted branches and shadowed builtins are outside it. ADR-0002 states this limit in its own `## Decision` and prices it as accepted; the compensating read was done by `verify` and again here, over all twelve source and test files | none | `no-owner` |
| `verify`'s `## Not verified, and why`: AC3 is statistical and was observed once; a correct implementation can in principle fail it. `plan.md` `## Risks` prices it below 10^-40 and the vision declines any claim about statistical quality | none | `no-owner` |
| `verify`'s `## Not verified, and why`: `BUG-0001` is filed, not fixed. It is already on the board at `ready`, where the orchestrator dispatches it to `plan` | plan | `item-filed:BUG-0001` |

## Verdict

**Accepted, closed under ADR-0004 v3's second bounded override, and merged.**

On the merits, unchanged from round 1 and re-confirmed here: eleven acceptance criteria met and
independently evidenced, three binding ADRs conforming on ten quoted `## Decision` clauses, a
record that reconstructs without gaps, a diff with nothing unrequested in it, and a trial merge
whose result is green. All thirteen Definition of Done criteria now pass — including D4, which
round 1 failed by its own act of filing `Q-004`, and D9, which was *not yet* only because the
close must precede the merge.

**The override, and its four conditions checked one at a time.** ADR-0004 v3 `## Decision`
point 4 authorises `review-close` to make `WI-0001`'s `in-review → done` transition with
`--force`. It is a second bounded override rather than a widening of point 3's: each names one
skill and one transition, which is the property that leaves the record able to show that
somebody looked twice rather than once.

| # | condition | held? |
|---|-----------|-------|
| 1 | a full `run-gate --skill review-close --item WI-0001 --all --resolving 'WI-0001:in-review->done'` first, with **every** verdict recorded in the journal entry | **yes** — run immediately before the transition; exit 1. Eight `PASS`, two `MANUAL` (this skill's own `definition-of-done` and `record-is-reconstructible`, both decided in this document), one `FAIL`. All eleven verdicts are in this execution's journal entry |
| 2 | `claims-are-sourced` is the only hard gate reported failing | **yes** — `run-gate: 1 hard gate(s) failed: claims-are-sourced` |
| 3 | exactly one error, matching point 3's four properties | **yes** — `lint-claims: 1 error, 0 warnings`. Code `claim.unsourced`; file `docs/product/vision.md`; section `## Engagement state`, confirmed by reading the file rather than inferred — the section opens at line 65 and the reported line 67 is its second bullet; sentence *"Three questions are open with them, all filed at intake"*. The coordinate reported is `:67`, and a line number is not one of the four properties, for the reason point 3 gives |
| 4 | the history reason names this ADR | **yes** — the row for this move names ADR-0004 and its point 4 |

Condition 1 is the whole of the mitigation for what `--force` costs, and the cost is real: the
override is all-or-nothing, so the ten other verdicts on the most consequential transition this
item makes rest on a run recorded beside the move rather than on the move's own gate run. A
reader who doubts them can re-run the one command, which is why it is written out above rather
than described.

**What this close does not do.** It does not repair `docs/product/vision.md:67`. The sentence is
still false and still uncited, it is still row one of the invalidation set disposed
`owned-by-ending`, and `lint-documents --rule engagement-state-is-restated --item WI-0001
--context work-item` still reports *NOT APPLICABLE* here. The ending owns it, and ADR-0004
point 4a bounds what follows: once this merge lands, `vision.md` matches the trunk and leaves
the `--changed-since` window `review-close`'s gate uses, so a later item that does not itself
edit the file will not meet this wall at its own close.

**The merge.** Closed first, then merged: `commits-reference-the-item` reads `main..wi/WI-0001`,
and merging first would empty the range the gate inspects. The merge sha is recorded by
`scripts/record-merge` in `item.md`'s `merge-commit`, which is where a fact created after the
closing entry belongs (`spec/journal-and-history.md` §2.2b).
