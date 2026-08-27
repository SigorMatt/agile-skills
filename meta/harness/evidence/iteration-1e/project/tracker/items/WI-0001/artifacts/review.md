# Review — WI-0001

## What I examined

- **The record's mechanics.** `history.md`: eight rows chaining `—` → `draft` →
  `awaiting-answer` → `draft` → `ready` → `planned` → `in-progress` → `verifying` → `in-review`,
  with no gap and a last row matching `item.md`. `journal.md`: eight entries, one per row, by
  `intake`, `refine`, `answer-questions`, `refine`, `plan`, `implement` twice and `verify` —
  read in full, not skimmed. All three questions `answered`, `answered-by: human`, each with a
  `## Consequences` list naming files that exist.
- **The diff**, `main..wi/WI-0001`, hunk by hunk rather than the reports about it: `__main__.py`
  (plan step 1), `money.py` (step 2), `store.py` (step 3), `cli.py`'s parser (step 4) and its
  handlers and single failure path (step 5), the three test modules (step 6), `README.md`
  (step 7). Every hunk traces to a step or a criterion; there is no hunk I could not place.
- **The two error paths the diff leaves open**, by running them: an unwritable store directory
  and a store path that is a directory. One of them is the finding below.
- **The reports' declared gaps** — `## What I did not do` in `impl-report.md` and
  `## Not verified, and why` in `verify-report.md` — each decided as acceptable or not, below.
- **The claims in `docs/` about what this item touched, from what they cite** (D12), listed in
  the table below. `docs/architecture/overview.md` v1 is the document this item produced; its
  absolute claims were checked against the code, not against the sentence.
- **The merge result**, on a throwaway branch off `main`, discarded afterwards.

### The D12 claim audit

Each claim was checked by opening the code it is about, not by re-reading the sentence or a
document repeating it.

| claim in `docs/` | what I opened | verdict |
|------------------|---------------|---------|
| `overview.md`: "no server, no daemon, no database and no network call" | every `import` line in `expenses/*.py`: `argparse`, `datetime`, `re`, `sys`, `json`, `os`, `pathlib`, `tempfile`, and the package's own modules. A grep for `socket|http|urllib|sqlite3|requests|subprocess` returns nothing | **true** |
| `overview.md`: "neither `store.py` nor `money.py` imports `cli.py` or prints anything" | both files, grepped for an import of `cli` and for `print(` — neither appears in either | **true** |
| `overview.md` / ADR-0002: "amounts are integers counting minor units, never floats" | `money.py` in full: no `float`, no `Decimal`, and the only `/` characters are the floor-division `//` in `format_amount` and a docstring | **true** |
| `overview.md`: "a missing file reads as an empty dataset" | `store.load`'s `except FileNotFoundError` branch, and the run of both listings against a path whose directory does not exist | **true** |
| `overview.md`: "every refusal writes to stderr, changes nothing on disk and exits non-zero" | `cli.main`'s single `except ExpensesError`, plus the nineteen refusals verification triggered and two I ran myself | **true of every refusal**, and the word is load-bearing: an operating-system error is not a refusal in this codebase's vocabulary, and it behaves differently. See `## Findings` |
| `overview.md`: "it stores no currency at all" | the record `store.add_expense` appends — `amount_minor`, `paid_by`, `shared_by`, `shares_minor`, `date`, `description` — and a grep for currency words and symbols across the package, which returns only the two regexes | **true** |
| ADR-0003: the remainder goes to the first-named sharers | `money.split_equally`, and the stored record for 10.00 over `Ana,Ben,Cara`: `{'Ana': 334, 'Ben': 333, 'Cara': 333}` | **true** |
| `vision.md`: "a record made by mistake can be deleted; it cannot be edited in place" | the command surface in `cli.build_parser` — `person add|list`, `expense add|list` and nothing else | **true today** — neither exists yet, and deletion is WI-0004's. The sentence describes the product, not the current build, and `vision.md`'s own text says so |

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | nine `- [x] AC` lines in `item.md`, zero `- [ ] AC` |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | the report's criteria table has a row per AC naming the command run and quoting its output; spot-checked AC4 (`cmp` plus two md5 hashes), AC6 (ten inputs with exit codes and stderr) and AC8 (two fresh stores compared) against the criteria's own wording |
| D3 | the item's gates passed on the final state of the code | **pass** | `implement` ran its gates on `4aae88d`; `verify` ran the suite itself on `fb54eef`; this review ran it again on the merge result. `check-verify-freshness` reports the only changes since `fb54eef` are ten files under `tracker/` |
| D4 | no open blocking question remains | **pass** | `Q-001`, `Q-002` and `Q-003` are all `status: answered` with `answered-by: human`; the board reports 0 open questions |
| D5 | a journal entry per execution; history chains without a gap | **pass** | eight history rows, eight journal entries, each entry's heading stamped by `journal-entry`; every `from` equals the previous `to`; the last row matches `item.md` |
| D6 | every design decision is in an ADR, cited from the plan or journal | **pass** | ADR-0001 (store), ADR-0002 (minor units), ADR-0003 (remainder), ADR-0004 (test command) — all four cited from `plan.md`'s `## Decisions and ADRs` table, and the two `refine` routed to `plan` are among them |
| D7 | documents the change invalidated are updated, with a version bump and a change-log row | **pass** | `docs/architecture/overview.md` was created at v1 by `plan` for this item, with a change-log row, and it describes what was actually built — checked claim by claim above. Nothing else was invalidated: `vision.md` v3 predates the code and says nothing the code contradicts, and the four ADRs are all v1 and current |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 8 commit(s) on main..wi/WI-0001 name WI-0001" |
| D9 | merged into the trunk, not left only on the branch | **pass** | the trial merge onto a throwaway copy of `main` was a clean fast-forward and the suite passed on the result; the real merge is performed by this execution immediately after the close, in the order the procedure requires, and its commit is named in this execution's journal entry |
| D10 | verification ran after the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: "verified at fb54eeff; wi/WI-0001 has moved to b10a9c9e but only the record changed (10 file(s) under tracker/ or docs/), so the verification still covers the code". Run, not assumed |
| D11 | `review.md` exists and states what was examined | **pass** | this document, whose `## What I examined` comes first and names the files, the diff range, the commands and the claims audited |
| D12 | claims in `docs/` about what this item touched are still true; absolutes carry a resolvable citation | **pass** | the eight-row audit above, each checked by opening what the claim cites. `lint-claims --changed-since main` → exit 0. A whole-tree run reports two pre-existing errors in `docs/product/vision.md`, which are BUG-0001 and are outside the scoping D12 defines |

## Findings

1. **`store.save` lets an operating-system error escape as a traceback, where `store.load` turns
   the same class of error into a refusal.** With the store pointed inside a directory the user
   cannot write to, `person add Ana` exits 1 with an eleven-line `PermissionError` traceback; the
   read path in the same situation exits 2 with `cannot read ...: [Errno 21] Is a directory`. Both
   were run. **Filed as BUG-0002 at `ready`, `found-in: WI-0001`, priority medium** — not sent
   back, because none of AC1 to AC9 covers an environment error, so a send-back would have had
   nothing to fail against and would have asked `implement` for behaviour with no criterion
   behind it. No data is at risk: the atomic-replace write leaves the previous dataset untouched.
2. **`cli.person_add` and `cli.expense_add` re-apply `.strip()` to the name they print.** The
   stripping rule belongs to `store.add_person`, which is also where it is tested. Today the two
   agree; the day the store's normalisation changes — casefolding, collapsing inner whitespace —
   the confirmation line will print something the store did not record, and nothing asserts on
   the confirmation line, so no test will notice. Not blocking, and not worth an item: the fix is
   to print what the store recorded rather than what the CLI computed, and it belongs to whoever
   next touches those two handlers.
3. **A dead branch in `money.parse_amount`.** In `int(fraction.ljust(2, "0") or 0)`, the `or 0`
   can never be reached: `"".ljust(2, "0")` is `"00"`, so the operand is always a non-empty
   string. Harmless, and it reads as though the empty case were possible when the regex has
   already excluded it. Not blocking.
4. **Nothing in the diff contradicts an ADR**, so no question was filed. The four deviations
   `impl-report.md` declares are each where it says they are, and each is in *how* rather than
   *what*: tests committed with their module instead of in one pass, `main` taking optional
   streams, `store` exposing `people`/`expenses`/`empty_dataset`, and the confirmation wording
   the plan explicitly left open.

## Accepted gaps

Each of these was declared by an earlier stage and is accepted here — with somewhere to live, so
that closing this item does not make it invisible.

| gap | declared in | why it is acceptable | where it now lives |
|-----|-------------|----------------------|--------------------|
| No lint runs on this code | `verify-report.md`, `impl-report.md` | the project may install nothing, and the standard library ships no linter; ADR-0004 records the decision and both gates recorded `skipped` rather than `pass` | ADR-0004, which says to supersede it if the constraint lifts |
| The default store location was never written to during verification | `verify-report.md` | verifying it for real would write into the account running the pipeline; the resolver's branches are unit-tested, and no criterion names a location | `verify-report.md` `## Not verified, and why`, and ADR-0001, which documents the order |
| Concurrent use by two processes is unprotected | both reports | out of scope for the epic by the vision's own statement, and no criterion asks for it | ADR-0001's consequences and `overview.md`'s "what this shape does not do" |
| A hand-edited data file is believed — shares are not re-checked against the amount on read | both reports | accepted deliberately in ADR-0003's consequences; the tool's own commands cannot produce such a file | ADR-0003 |
| `store.load` fills in missing `people`/`expenses` keys instead of refusing | `verify-report.md` `## Observations` | unreachable through the tool's own commands, since `save` always writes both; it changes nothing anyone can currently observe | recorded here and in the verification report, for whoever adds a second writer in WI-0003 or WI-0004 |
| Two unsourced absolutes in `docs/product/vision.md` | `impl-report.md` `## What I did not do` | outside the scoping D12 defines, and outside every contracted gate | **BUG-0001**, filed at `ready` |

## Verdict

**Accepted.** WI-0001 meets all twelve Definition of Done criteria. The change is what the plan
described and what the criteria asked for, the record supports reconstructing it without this
session, and the trial merge is clean with the suite green on the merge result. Two defects found
during review belong elsewhere and are filed as BUG-0001 and BUG-0002 rather than held against
this item; three findings are recorded above and none of them blocks.

The item is closed `done` with `outcome: delivered`, and the branch is then merged into `main`.
