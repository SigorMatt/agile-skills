# Review — WI-0005

## What I examined

- **The diff, hunk by hunk**, not the reports about it: `git diff main..HEAD -- envel/ tests/ docs/`
  — nine hunks across five files. Every one maps to a plan step, and nothing in it serves neither
  a criterion nor a step:

  | hunk | file | serves |
  |------|------|--------|
  | `@@ -24,7` | `envel/cli.py` | step 6 — the `metavar` gains `fix` and `remove` |
  | `@@ -94,9` | `envel/cli.py` | step 6 — the two subparsers and their options |
  | `@@ -112,6` | `envel/cli.py` | step 7 — the *no option given* check, above `store.load` |
  | `@@ -137,6` | `envel/cli.py` | step 8 — the two dispatch branches |
  | `@@ -289,3` (+190) | `envel/envelopes.py` | steps 1–5 — `find_entry`, `envelopes_below_zero`, `correct`, `remove` and the two success lines |
  | `@@ -8,6` (+1) | `tests/test_cli.py` | step 10 — the `re` import |
  | `@@ -1353,3` (+475) | `tests/test_cli.py` | step 10 — `class Corrections`, 30 end-to-end cases |
  | new, 414 lines | `tests/test_corrections.py` | step 9 — 8 classes, 38 cases over the operations |
  | four hunks | `ADR-0002` | step 11 — the one `to-update` invalidation entry |

  `envel/summary.py`, `envel/store.py`, `envel/money.py` and `envel/dates.py` are absent from the
  diff, which is what the plan said would be true if the design held.

- **The record's mechanics.** `history.md` chains without a gap — ten rows from creation to
  `in-review`, with `draft → awaiting-answer → draft` twice for refinement's two question rounds —
  and its last row matches `item.md`'s status. Ten history rows imply ten executions and
  `journal.md` carries ten entries, one per execution, in the same order with the same actors and
  timestamps. All twenty criteria are `- [x]`; `grep -c '^- \[ \]\|^- \[~\]'` returns 0. All eight
  questions on the item are `answered`, `answered-by: human`, with `## Consequences` naming files
  that exist.

- **All eleven ADRs, in full**, and `docs/architecture/overview.md` and `docs/product/vision.md`.

- **`## Not verified, and why`** in the verification report and **`## What I did not do`** in the
  implementation report — eleven declared gaps between them, each dispositioned below.

- **D12, audited from the citations rather than from the prose.** Each row names what I opened and
  what a counterexample would have looked like. Two were run at this review, at the boundary
  rather than the happy path.

  | claim | where | what I opened | Falsifier | verdict |
  |-------|-------|---------------|-----------|---------|
  | *"`entries` is ordered as written … an envelope's balance is the sum of `cents` over the entries naming it — the second half with no branch on `kind`"* | `ADR-0002` `## Decision`, as rewritten at v4 | `envel/envelopes.py:63`, `balance` — one `sum` over the entries naming the envelope, with no `kind` test; and the ordering, by correcting the **first** entry of a three-entry store and reading the list back | An entry that changed position, or a `kind` branch inside `balance`. Correcting the first entry is the case where an implementation that rebuilt the list would reorder it: the refs read `[1, 2, 4]` before and `[1, 2, 4]` after | **holds** |
  | *"the file is readable and repairable in any text editor"* | `ADR-0002` `## Consequences` | The store file itself — the envelopes' `created` stamps were edited by hand to set up an August summary, and the tool read the result back and printed from it | A store the tool refuses after a hand edit that keeps the schema. It did not refuse | **holds** |
  | *"The counter is the only source of a new reference. Nothing derives one from a position, a length or a maximum"* | `ADR-0010` `## Decision` 5 | Every place in `envel/` that writes a `ref` or `next-ref`, enumerated with `grep -n 'ref"\]\|"ref":\|next-ref\|take_ref' envel/*.py` → 21 lines, of which the writes are `envelopes.py:50`, `:111`, `:173`, `:270`, `:276` and `store.py:36`, `:53`, `:55`, all eight predating this branch. Then the behaviour, at the boundary | Removing the **highest**-numbered entry and then recording a new one — the only case where a derived counter is invisible. A store at `refs [1,2,3] next-ref 4`: after `envel remove 3` → `refs [1,2] next-ref 4`, and the next spend took **4**. A maximum- or length-derived counter would have reissued `3` | **holds** |
  | *"`on` is present on every spend entry … never absent and never null"*, and *"`description` is present only when one was typed"* | `ADR-0006` `## Decision` | `correct`'s write path: `on` is only ever **set**, at `envel/envelopes.py:386`, and no line in `envel/` deletes one; `description` is removed by `pop` at `envel/envelopes.py:389` | A spend left without `on`, or carrying `description: ""`. `envel fix <ref> --on ""` is refused by `dates.parse_date`; after a correction setting all four fields with `--description ""` the stored entry reads `'on'` present and non-null and `'description'` absent | **holds** |
  | *"No field links the two entries to each other"* | `ADR-0007` `## Decision` | `grep -n '"move"' envel/*.py` → 11 lines; this change adds two, `envel/envelopes.py:351` and `:442`, each reading `entry["kind"]` on the entry it was handed | A refusal that named the *other* envelope, or that reached ref 7 while asked about ref 6. Both messages name only the entry given, and refusing 7 produces the same sentence about 7 | **holds** |
  | *"Amounts are printed with exactly two decimal places and no currency symbol"* | `overview.md` `## Conventions` | The output at the two boundaries a two-decimal rule can fail on — a whole number of units and a zero balance. `envel fix 4 --amount 5` yields the line `4  2026-09-06  spend  groceries  -5.00  shop`; a freshly created envelope lists as `z  0.00` | An amount printed as `-5` or `0`. Neither appeared; both went through `money.format_amount`, and `grep` over the branch's added lines finds no `float(`, `/ 100`, `% 100` or `.2f` anywhere | **holds** |
  | *"write the whole store back, atomically, but only if something changed"* | `overview.md` `## The shape of it`, beat 3 | Both sides, run at this review. A **refused** `envel fix 999 --amount 1.00`: the file's mtime does not move. A **successful** correction that changes nothing — `envel fix 4 --amount 12.50` on an entry already at 12.50, against a tool-written file: exit 0, and the file's mtime **does** move while its content stays byte-identical (`aca4fa64…` before and after) | A refusal that wrote — none did, across every refusal in the verification report and the eleven AC19 combinations. The no-op success is the narrower case and is the one I went looking for: `envel fix` is the first command in this tool that can succeed while changing nothing | **holds**, with the reading narrowed — see `## Findings` |
  | *"the number an entry is given stays that entry's, so a number written down last week still means what it meant"* | `vision.md` `## What it is for` | The same boundary as the `ADR-0010` row: the highest entry removed, then a new one recorded | A reissued number. `4` was issued once | **holds** |
  | The correction and income paragraphs — four fields on a spend, removal that says what it took, the shortfall named, moves excluded; amount and envelope on an income, no date, same command, no flag | `vision.md` `## What it is for` | Each clause against a command run here: AC2–AC5, AC11, AC9, AC13, AC16, AC17, AC18 | A clause the tool contradicts. `--income` is `unrecognized arguments`; `--on` on an income is refused; the shortfall message names the envelope, what it holds and how short it falls | **holds** |

- **The trial merge and its result**, recorded under `## Verdict`.
- **`tracker/waiting/EP-001.md`** — deliberately not read: it is the epic's, and this is an item
  close.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion settled | **pass** | 20 of 20 are `- [x]`; `grep -c '^- \[ \]\|^- \[~\]'` returns 0. No substitution was taken, so no criterion owes a question about its wording |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | The `## Criteria` table has one row per AC1–AC20, each naming a command and quoting its actual output. Four were spot-read against the report and against the tool: AC9's `groceries holds 197.50, and this change would leave it 90.00 short.`, AC17's `removed entry 8, 50.00 from savings. savings now holds 0.00`, AC6's `usage: envel fix` at exit 2, AC20's `2026-07: 0, 2026-08: 1, 2026-09: 0` |
| D3 | gates passed on the **final** state of the code | **pass** | `check-verify-freshness WI-0005 wi/WI-0005` → exit 0: *"verified at 1695487b; wi/WI-0005 has moved to 62f02d98 but only the record changed (5 file(s) under tracker/ or docs/)"*. The suite was re-run by this review on the merge result: 299 tests, exit 0 |
| D4 | no open **blocking** question | **pass** | All eight questions on the item are `answered`. `Q-009`, filed by this execution, is `blocking: false` |
| D5 | a journal entry per execution, history chains | **pass** | Ten history rows, ten journal entries, matching actors and timestamps; the last row's `to` is `in-review`, which is `item.md`'s status |
| D6 | every design-changing decision is in a cited ADR | **pass** | One decision changed the design — a correction edits the entry in place and a removal deletes it — and it is `ADR-0011`, written by `plan` and cited from `plan.md`'s `## Approach`, `## Decisions and ADRs` and `## Binding ADRs`, and from the `plan` journal entry. The four reversible assumptions sit in `plan.md`'s `## Assumptions` with their reversal costs, each correctly **not** an ADR |
| D7 | the invalidation set is disposed and confirmed | **pass, with a finding** | `## Invalidation set confirmation` below, including the answer to the question the set cannot answer for itself |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0005 wi/WI-0005` → exit 0, *"all 5 commit(s) on main..wi/WI-0005 name WI-0005"* |
| D9 | merged into the trunk | **pass** | Trial-merged and tested, discarded, then merged for real after this close; the sha is in `item.md`'s `merge-commit`, written by `scripts/record-merge` |
| D10 | `verify` ran **after** the last code change | **pass** | Same evidence as D3. `Verified-commit: 1695487b4a9962308019729f446b21ae2f216e11` is the last commit touching `envel/` or `tests/`; the two commits after it change only `tracker/` |
| D11 | `review.md` states what was examined, every accepted gap dispatchable | **pass** | `## What I examined` comes first and names the hunks, the audits and the boundaries chosen. `## Accepted gaps` disposes all eleven, and the one carrying work is `question-filed:WI-0005/Q-009`, filed **before** this close |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass** | Nine audit rows above, each naming what was opened and its falsifier, two run at this review at the boundary. `lint-claims --context work-item --changed-since main` → exit 0 over *"1 document(s) in 1 path(s) differ from main (73a5c7a) under docs"* — a scope that is not empty and contains `ADR-0002`, the one document this branch wrote |
| D13 | the plan's `binding-adrs` list is **complete** | **pass** | The list names `ADR-0001` … `ADR-0011`, which is **every** ADR in the workspace: `find docs/architecture/adr -name '*.md'` returns exactly those eleven. A list naming the whole index cannot omit an ADR the change engages. Whether the change *conforms* to each is `verify`'s verdict, and all eleven are recorded `conforms` there with a clause quoted from each `## Decision` |

## Invalidation set confirmation

All 29 entries carry a disposition, and `lint-documents --rule invalidation-set-is-disposed --item
WI-0005` → exit 0 over *"29 invalidation entr(y/ies) against 29 row(s) in the verification
report"*.

| document | disposition | confirmed by |
|----------|-------------|--------------|
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — the `entries` bullet | `to-update` | **Updated, with both required marks.** `version: 3 → 4`, `updated-for: WI-0005`, a `## Change log` row for v4 and a `## Corrections` row of kind `erratum` naming the clause replaced and why. The new text was read against the code here — the first D12 audit row above |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — `## Consequences` and Reversibility | `verified-still-true` | Reopened. The reversibility clause is about the document's **shape**, and no key was added, removed or renamed: the stored document's keys are `['entries','envelopes','format','next-ref']`, an entry's are `['at','cents','envelope','kind','on','ref']`, `FORMAT` is still `2` at `envel/store.py:11`, and `envel/store.py` is absent from the diff |
| `ADR-0010` ×2, `ADR-0007`, `ADR-0006`, `ADR-0009`, `ADR-0008`, `ADR-0001`, `ADR-0003`, `ADR-0004`, `ADR-0005` | `verified-still-true` | Each reopened in `verify-report.md`'s `## Invalidation set` with an enumeration, the members and a falsifier. Four were re-audited independently here with the boundary chosen rather than the happy path — the `ADR-0010`, `ADR-0006`, `ADR-0007` and `ADR-0002` rows above |
| `docs/architecture/overview.md` ×11 | `verified-still-true` | Reopened in the verification report; two re-audited here — `## Conventions`' two-decimal rule at the zero and whole-number boundaries, and `## The shape of it`'s beat 3 on both its refusal and its no-op-success side. The `## What is not decided yet` row's universal over `EP-001`'s items is still true: the board carries six items and no bug was filed by `implement`, by `verify` **or** by this review |
| `docs/product/vision.md` ×4 | `verified-still-true` | The two `## What it is for` paragraphs re-read clause by clause against commands run here; the reference sentence checked at the removal boundary; the no-network clause against the fifteen-line import enumeration |
| `docs/architecture/overview.md` — `## Engagement state` | `owned-by-ending` | **Left alone, confirmed mechanically.** `git diff main..HEAD -- docs/architecture/overview.md` is empty: this item did not edit the file at all |
| `docs/product/vision.md` — `## Engagement state` | `owned-by-ending` | **Left alone.** `docs/product/vision.md` is absent from `git diff --stat main..HEAD` |

### Did this change falsify a document the set does not name?

**Yes, in one respect — and it is the one document the set structurally could not name.**

The workspace holds thirteen documents under `docs/`. The invalidation set names twelve. The
thirteenth is `docs/architecture/adr/ADR-0011-a-correction-edits-the-entry-in-place.md`, written by
**this item's own `plan`** from the design this change implements. A set lists the documents a
change could make false; a document the plan writes from that same change is not a candidate for
its own list.

I read `ADR-0011` in full against the branch head. Every clause of its `## Decision` is true of the
code, and `verify` records `conforms` for it with the clause quoted. What is **not** right is one
of its citations: `## Decision` 5 says *"`envel/cli.py` writes nothing … [src: envel/cli.py:165]"*,
and this change moved `if result.changed:` from line 165 to line **217**. On the branch head, line
165 is `elif arguments.command == "spend":`. The same drift hit
`tracker/items/WI-0005/artifacts/plan.md` at lines 44 and 210.

The sentences are true and the pointers are wrong, which is the harder of the two failures to
notice: the line exists, so the citation **resolves**, and `validate-workspace`, `lint-claims` and
`lint-documents` all pass over it. `verify` found it, recorded it in `## Defects found`, and
correctly declined to act — not a criterion failure, not a defect in delivered behaviour, and
`verify` writes no document. This review meets the same three walls and takes the fourth route the
procedure provides: `WI-0005/Q-009`, non-blocking, addressed to the architect, filed before this
close and disposed below.

Nothing else among the twelve named documents was found false, and the enumeration above is what
that claim is made against rather than a memory.

## Sections restated at the ending

`not an ending` — this is an item close. `lint-documents --rule engagement-state-is-restated --item
WI-0005 --context work-item` reports *"NOT APPLICABLE — an item close is not an ending, and the
sections are the ending's"*, and both sections were confirmed untouched under D7.

## Findings

1. **`envel fix` is the first command in this tool that can succeed while changing nothing, and
   `overview.md`'s beat 3 now reads more narrowly than it did.** *"Write the whole store back,
   atomically, but only if something changed"* is gated on `result.changed`, which `correct`
   reports `True` for unconditionally once past its refusals. Measured here: `envel fix 4 --amount
   12.50` on an entry already holding 12.50 exits 0 and rewrites the file — mtime moves — with
   **byte-identical** content. No reader of the store can tell, and the refusal half of the
   sentence is exactly true (a refused `fix` does not move mtime). Recorded rather than acted on:
   the sentence is true of everything a reader can observe, no criterion speaks to a no-op
   correction — `refine` listed it among the three combinations deliberately left unconstrained —
   and narrowing the overview's wording over an unobservable write would be a decision this item
   was not asked to take. A reader now has the measurement.

2. **`correct` decides an entry is income by the *absence* of `on`, and then says so in words.**
   `if "on" not in entry and (on is not None or description is not None)` produces the message
   *"entry N is income, which carries no date and no description"*. Today that is sound and
   deliberate: `ADR-0006` makes `on` present on every spend and absent on every income, moves are
   refused two lines earlier, and the docstring says the rule is read off the entry rather than off
   its kind — the same idiom `ADR-0002` uses to keep `balance` free of a `kind` branch. The note is
   for the next person: the *message* asserts a kind from an absence, so a future entry kind
   carrying no `on` would be reported to the user as income. Adding a kind is a design decision
   that goes through `plan`, and `ADR-0006` is where it would be caught, so no work is deferred.

3. **No finding against the change itself.** `correct` takes six positional parameters, four of
   them nullable, which is at the edge of comfortable — but it is the shape `record_spend` and
   `move` already have in the same module, and inventing a second convention for one function
   would be worse than the mild awkwardness. The refusal ordering carries its reasoning in the
   docstring rather than leaving it to be re-derived. No duplicated rule, no swallowed error, no
   name that says something untrue.

## Accepted gaps

Eleven, from the verification report's `## Not verified, and why` and the implementation report's
`## What I did not do`. The `disposition` column carries the machine-readable value only; each
gap's reasoning sits in the `gap` column with it.

| gap | owner | disposition |
|-----|-------|-------------|
| Three `envel/cli.py:165` citations that this change pushed off their line — `plan.md:44`, `plan.md:210` and `ADR-0011:101`. The only one of these eleven that carries work, and the only one filed | `answer-questions` | `question-filed:WI-0005/Q-009` |
| `envel fix " 4 "` — a reference with surrounding whitespace — succeeds, because `int()` strips it. No criterion speaks to it either way: AC1 promises a refusal for a reference that *matches no entry*, and this one matches. A limitation recorded, not work deferred | none | `no-owner` |
| A correction to the value the entry already has succeeds and prints. `refine` recorded it in the item's R10 table as deliberately unconstrained, `implement` declared it, and this review measured it — finding 1. The stakeholder has never asked for it to refuse | none | `no-owner` |
| `--envelope` naming the envelope the entry is already in succeeds and prints the single-envelope line. Same R10 row; it is the identity case of AC5, whose arithmetic it satisfies trivially | none | `no-owner` |
| `--on` setting a date before the envelope existed succeeds, and the entry then shows in `envel entries` for a month whose summary says no envelopes existed. Same R10 row, and **not new**: `envel spend groceries 5.00 --on 2026-01-05` reaches the identical pair of outputs on `main`, which `verify` established in a worktree at `main`. It is `WI-0003` AC7 meeting `WI-0006`'s listing, and neither criterion is false | none | `no-owner` |
| AC19's six combinations with no standing executable case — the refusals of AC1, AC6, AC9, AC10, AC13 and AC18. `verify` waived them by name: AC19 is one mechanism in two lines, `envel/envelopes.py:378` and `envel/cli.py:217`; the three `UnchangedOnRefusal` cases pin it where a mutation of the caller's document is visible by deep equality; and all nine combinations were verified by hand at verification. A test-coverage preference, not an obligation | none | `no-owner` |
| AC8's month-crossing case is observed against a store whose envelope timestamps were seeded by hand. `envel new` stamps `created` with today and `WI-0003` AC7 gives a summary row only to an envelope that existed by the end of the month, so the observation AC8 names is unreachable otherwise; `tests/test_cli.py::Entries` already seeds this way. The correction and both summaries are the tool's | none | `no-owner` |
| Durability beyond a process boundary is untested — nothing exercises a power failure mid-write. `ADR-0002`'s atomic-replace claim is outside this item's criteria and outside its diff, and `envel/store.py` is byte-identical to `main` | none | `no-owner` |
| No repair for a hand-damaged `next-ref`. `ADR-0010` explicitly left that to whoever meets one, and nothing in this item meets one | none | `no-owner` |
| `implement` ticked no acceptance criterion. Not a gap at all but the division of labour, listed because the implementation report declares it: `verify` ticked all twenty against its own commands | none | `no-owner` |
| `implement` did not repair the two `vision.md` paragraphs sourced to the stakeholder's answers — and that was the right call. Both are the stakeholder's own words, both are now true rather than overtaken, and both were re-read clause by clause here | none | `no-owner` |

## Verdict

**Accept, and close as `delivered`.**

Twenty of twenty acceptance criteria are settled and each cites a command `verify` ran with its
output quoted. Every hunk of the diff serves a plan step. All thirteen Definition of Done criteria
pass. The eleven binding ADRs are the whole ADR index, so D13's completeness question answers
itself, and `verify` records `conforms` for each with a clause quoted from its `## Decision`. All
29 invalidation entries are disposed; the one document the set could not name was read here and
produced this review's only dispatched finding.

Trial merge, in order: `git worktree add --detach` a throwaway checkout of `main`, `git merge
--no-ff wi/WI-0005` → merge commit `4bb7630a7497ccab4b3c62a7228882c48eaaa433`, `python3 -m
unittest discover -s tests -t .` **on the merge result** → exit 0, `Ran 299 tests in 40.261s`,
`OK`. Trial discarded with `git worktree remove --force`, after which `git rev-parse main` returns
`73a5c7a601f80c76edcf3cc0de0b11596ac83bc8` — the same sha it returned before the trial, so the
trunk did not move.

This item is the last of `EP-001`'s six, and closing it does **not** end the engagement:
`WI-0005/Q-009` is open, so `scripts/engagement-state EP-001` cannot report `at-rest`. The ending
belongs to the execution dispatched once that question is answered.
