# Review — WI-0006

This is the **second** review of this item. The first rejected it on one finding — `F1`, a
docstring in `envel/summary.py` that shipped the claim this same item had struck from `ADR-0007` —
and sent it to `in-progress`. `implement` fixed it, `verify` re-verified the whole item at the new
head, and this review is of that state. The previous review's text is in git at `c7d4778`.

## What I examined

- `item.md` — fifteen criteria, all `- [x]`, none `- [ ]` and none `- [~]`; status `in-review`.
- `history.md` — **eleven** rows, chaining `draft → awaiting-answer → draft → ready → planned →
  in-progress → verifying → in-review → in-progress → verifying → in-review` with no gap; the last
  row matches `item.md`.
- `journal.md` — **eleven** entries, one per history row, actor and timestamp matching each.
- All four questions on the item: every one `answered`, each `## Consequences` naming real files.
- `plan.md` — nine steps, the AC mapping, four assumptions, the 29-row invalidation set,
  `deliverable-documents: none`, ten binding ADRs.
- `impl-report.md` — both rounds, in particular round 2's `## Gates`, `## Documents` (none) and
  `## What I did not do`.
- `verify-report.md` — rewritten for round 2, `Verified-commit: 226ceb58…`, in particular
  `## AC14 — the read`, `## Test sensitivity check` and `## Not verified, and why`.
- **The diff itself**, `main..wi/WI-0006`, hunk by hunk: 5 files under `envel/`, 4 under `tests/`,
  6 under `docs/`. And separately `c7d4778..HEAD`, which is this round's whole change: one hunk.
- `docs/architecture/adr/ADR-0001` … `ADR-0010`, for D13, and `ADR-0007` in full for the finding.
- `tracker/items/WI-0005/item.md` AC13, which `ADR-0007`'s amended `## Decision` makes a claim about.

### The send-back's own subject, checked first

`envel/summary.py` `entry_kind`, `c7d4778..HEAD`:

```diff
-    A move is stored as two entries with opposite `cents` and nothing linking them
-    (ADR-0007), so which side of one this is is read off the sign and from nowhere
-    else — the same thing that makes a balance a plain sum with no branch on the kind.
+    A move is stored as two entries with opposite `cents` (ADR-0007). No field names the
+    pair; since ADR-0010 the two halves do take consecutive references, and no code reads
+    that adjacency as a link. Which side of a move this is comes off the sign because the
+    sign is all this function needs — the same thing that makes a balance a plain sum
+    with no branch on the kind — and not because the other half could not be found.
```

Each of the three claims against what it restates, and against the code:

| claim | restates | checked |
|-------|----------|---------|
| *No field names the pair* | `ADR-0007` `## Decision`: *"**No field links the two entries to each other**"*; `overview.md`: *"No field in the file names the pair"* | a store the tool wrote: both `move` entries carry `kind`, `envelope`, `cents`, `on`, `at`, `ref` and nothing else |
| *since ADR-0010 the two halves do take consecutive references* | `ADR-0007`: *"Since `ADR-0010` … the two halves do carry **consecutive references**"* | `envel/envelopes.py:264`–`:266` and the two `take_ref` calls below them; observed as refs 4 and 5, the outgoing side first |
| *no code reads that adjacency as a link* | `ADR-0007`: *"no code pairs them by it"*; `overview.md`: *"No code reads that adjacency as a link"* | `grep -rn "ref" envel/ \| grep -E "ref *[-+] *1"` → **exit 1, no output** |

`grep -rn "nothing linking\|not linked\|linking them\|no link" envel/ tests/` → **exit 1**. The
struck sentence is gone from the source and appears nowhere else.

### F2's category, deepened this round

The previous review's F2 observed that nothing in the pipeline reads **source comments** for stale
claims, and that F1 was found only because a reviewer read the diff. So this round I read every
absolute claim this branch added to a comment or docstring under `envel/`, not only the one that
was sent back. Six were checkable and all six hold:

| claim, in source | checked |
|------------------|---------|
| `envel/dates.py:33`–`:35` (new): `DAY_LENGTH` *"Written once, used by day_of"* | defined at `:35`, read at `:93`, nowhere else. True |
| `envel/dates.py:90` (new): *"This is the only place that ten is written"* | `grep -n "10" envel/dates.py` → one hit, `DAY_LENGTH = 10`; `grep -rn "\b10\b" envel/*.py` outside `dates.py` → exit 1. True |
| `envel/dates.py:34` (new), quoting the module docstring: *"this module is the only place text and calendar days meet"* | the docstring's own next sentence scopes it — *"the only conversions between that text and a `datetime.date`"*. `envel/envelopes.py:33` `now()` formats a `datetime.**datetime**` into a timestamp, which is a moment and not a calendar day, and no other module builds a `datetime.date`. True as scoped, and the scoping sentence predates this branch |
| `envel/envelopes.py:44`–`:46` (new): *"The counter … is the only source of a new reference: nothing derives one from a position, a length or a maximum"* | no `max(`, no `len(` and no index in the reference path; `take_ref` reads `store["next-ref"]` and nothing else. True — and `verify`'s M1 shows the **tests** cannot yet tell this from a derived number, which is the accepted gap below, not a false comment |
| `envel/envelopes.py:264`–`:266` (new): the two halves take consecutive references, outgoing first, and which is lower is not observable | refs 4 then 5 with the outgoing side first, and AC6 asks only that both lines exist with opposite directions. True |
| `envel/store.py:96`–`:97` (new): *"the file is written only when a command reports that it changed something, so a listing never rewrites a store it was only asked to read"* | `grep -rn "store\.save" envel/*.py` → **one** call site, `envel/cli.py:166`, under `if result.changed` at `:165`. Boundary: a format-1 store — the one the read upgrades in memory — was listed and its md5 was unchanged. True |

No finding. F1 was the only sentence of its kind in the branch, and this is the read that says so
rather than assuming it.

### Claim audit (D12)

Each absolute claim this item wrote or repaired under `docs/`, decided by opening what it cites.
`docs/` is byte-identical to the previously verified commit, so these are the same eight sentences
the first review audited — and they were opened again here, not carried.

| claim | opened | falsifier | verdict |
|-------|--------|-----------|---------|
| `overview.md` `## The data`: *"No field in the file names the pair … the two consecutive references they take … No code reads that adjacency as a link"* | `envel/envelopes.py` `move`, `envel/summary.py` in full, and a store the tool wrote | a pairing field in a written store, or code indexing `ref ± 1`. The store's two move halves carry `ref` 4 and 5 and no pairing field; the grep returns nothing | **holds** — and the source now agrees with it, which is what F1 was about |
| `overview.md` `## The data`: *"An entry's `at` … A spend and a move each carry one field more"* | a store with all three kinds, including an **undescribed** spend | a kind carrying two extra fields. `move − income = ['on']`, exactly one; `spend − income = ['description', 'on']` on a described spend — two, but `description` is optional and predates this item. Checked **at the boundary**: an undescribed spend differs by exactly `on` | **holds**, with the imprecision noted at F3 |
| `ADR-0007` `## Decision`: *"No field links the two entries to each other"*, and the scopes it gives `WI-0006` and `WI-0005` | `WI-0006` AC2 and `WI-0005` AC13 and `Q-005` | an item whose scope is narrower than the ADR claims. `WI-0006` AC2 lists *"income, spend, or a move in or out"*; `WI-0005` AC13 refuses a correction aimed at a move and `Q-005` reaches income. Both match | **holds** |
| `ADR-0008` `## Consequences`: *"Nothing **derives** the carried-in figure from the other three"* | `envel/summary.py` `balance_before` (`:191`) and `bounded_balance` (`:182`) | a subtraction of the other three figures. There is none: it is a filtered sum with the bound moved to `< month`. Boundary: `verify`'s M3, widening the bound to `<=`, fails 4 tests, so the bound is load-bearing | **holds** |
| `ADR-0009` `## Decision`: the module holds this project's reports | `envel/summary.py`, and `ls envel/` | a third report elsewhere, or a report absent from this module. `summarise` and `list_entries` are both here and there is no other reporting module | **holds** |
| `ADR-0002` `## Decision`: the `format` bullet, now citing `ADR-0010` | `envel/store.py:11` (`FORMAT = 2`), `:17` (`READABLE = (1, 2)`), `:83` (the check on load) | `format` not checked on load. It is, at `:83` | **holds** |
| `vision.md`: *"read off the listing rather than remembered — off one envelope's entries, or off the month's across the envelopes"* | `WI-0005/Q-001` and `WI-0006/Q-003` in full, and both invocations | a stakeholder answer that says the envelope is required. `Q-003`'s answer is the opposite; `Q-001` never addressed it | **holds** |
| `vision.md`: *"one number counted once across everything recorded"* | a store the tool wrote across three envelopes | a per-envelope restart or a reused number. Refs ran `1..11`, all distinct; `fun`'s first is **3** and `car`'s is **7** | **holds** |

`scripts/lint-claims --context work-item --changed-since main` → exit 0. **Scope, from its own
output:** *"checked absolute claims: 6 document(s) in 6 path(s) differ from main (52a6237) under
docs; citations: every markdown file in the workspace"* — the six documents this change wrote,
which is the window that could have found something.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every checkbox settled | **pass** | 15 of 15 `- [x]`, 0 `- [ ]`, 0 `- [~]` |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | its round-2 `## Criteria` table has a command run at this head and its actual output for each of AC1–AC15. Spot-checked three by re-running them myself: AC9's arithmetic (0.00 − 34.99 − 12.50 − 20.00 = −67.49, printed), AC12's refusal (stderr, exit 1, empty stdout) and AC13's five refusals |
| D3 | gates passed on the final state | **pass** | `implement`'s round-2 transition ran all nine **unforced** and `verify`'s ran all nine unforced — neither needed `--force`, because this round wrote no document and so produced no version row for `doc.changelog.no-execution` to fire on. I re-ran the four command-backed ones here on `9aec7c1`: tests exit 0 (231), lint exit 0, `validate-workspace` 0 errors, `check-commit-refs` exit 0 |
| D4 | no open blocking question | **pass** | all four questions on the item are `answered`; 33 of 33 in the workspace |
| D5 | a journal entry per execution, history chains | **pass** | 11 rows, 11 entries, matched by actor and timestamp |
| D6 | design decisions in an ADR, cited from the plan | **pass** | `ADR-0010` is the one design decision this item forced, cited 9 times in `plan.md`, argued with three options and an explicit reversibility verdict. Round 2 forced no new decision — it corrected a comment to match a decision already recorded |
| D7 | invalidation set disposed; plus what the set does not name | **pass** | see `## Invalidation set confirmation` |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0006 wi/WI-0006` → *"all 9 commit(s) on main..wi/WI-0006 name WI-0006"* |
| D9 | merged into the trunk | **pass** | trial-merged into a detached worktree of `main` at `4615396`, `python3 -m unittest discover -s tests -t .` → exit 0 with 231 tests and `compileall` → exit 0 **on the merge result**; trial discarded and `git rev-parse main` confirmed still `52a6237`. Merged for real after the close, sha recorded by `scripts/record-merge` |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness` → *"verified at 226ceb58; wi/WI-0006 has moved to 9aec7c11 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"*. Confirmed independently: `git diff --name-only 226ceb5..HEAD -- ':!tracker' ':!docs'` is empty |
| D11 | the review record exists and says what was examined | **pass** | this document; every accepted gap disposed below |
| D12 | claims in `docs/` about the touched behaviour are still true | **pass** | the audit table above: eight claims, each decided from what it cites, each with a falsifier, two checked at a boundary. Plus the six source-comment claims under `## F2's category, deepened this round`, which D12 does not require and F2 says somebody should |
| D13 | the plan's `binding-adrs` list is complete | **pass** | the list names `ADR-0001` through `ADR-0010`, which is **every ADR in `docs/architecture/adr/`** — `ls docs/architecture/adr/*.md` is ten files. No ADR can be engaged and unlisted. `verify`'s ten conformance verdicts are in `verify-report.md` and are not re-decided here |

## Invalidation set confirmation

| document | disposition | confirmed by |
|----------|-------------|--------------|
| `docs/architecture/overview.md` (11 entries) | 1 `to-update`, 9 `verified-still-true`, 1 `owned-by-ending` | version **8** with a change-log row (8 rows for 8 versions). `verify` reopened the nine at this head and I re-read three against the diff. The `## Engagement state` section is **byte-identical** to `main`: md5 `6fd22866…` on both, measured between the heading and the next `## ` |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` (4 entries) | 1 `to-update`, 3 `verified-still-true` | version **3** with a change-log row and a `provenance` entry in `## Corrections`. One of the three is the row `implement` **added on discovering it** — a sentence in the append-only `## Corrections` section that this change made stale and which may not be edited. I agree with the disposition and with recording it rather than repairing it |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | `to-update` | version **3**, two change-log rows and two `erratum` entries, each quoting the removed text verbatim. **This entry was the origin of the first review's finding**, and the finding was in the source rather than in this document — which was already correct. Re-read in full here |
| `docs/architecture/adr/ADR-0008-…-filtered-sum.md` | `to-update` | version **2**, change-log row and `erratum`. Checked at the boundary via `verify`'s M3 mutation |
| `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` | `to-update` | version **2**, change-log row and `erratum` |
| `docs/architecture/adr/ADR-0001`, `ADR-0003`, `ADR-0004`, `ADR-0005`, `ADR-0006` | `verified-still-true` | `verify` reopened each with its own enumeration at this head; I checked two against the diff — `ADR-0003`'s path claim (no path knowledge outside `envel/store.py`, grep exit 1) and `ADR-0001`'s conversion claim (no digit arithmetic outside `envel/money.py`, grep exit 1) |
| `docs/product/vision.md` (5 entries) | 1 `to-update`, 3 `verified-still-true`, 1 `owned-by-ending` | version **7** with a change-log row. The `## Engagement state` section is **byte-identical** to `main`: md5 `4c18d819…` on both |

**Did this change falsify a document the set does not name?** No, and the answer is by enumeration
rather than memory. `ls docs/**/*.md` is **twelve** files: `overview.md`, `vision.md` and ten ADRs.
The set names eleven of them and `ADR-0010` is the twelfth, written by this item's plan. I read
`ADR-0010` against the delivered code — its five numbered decisions each hold, including the
in-memory upgrade, which I checked by listing a format-1 store and finding its md5 unchanged. There
is no document under `docs/` outside the set plus `ADR-0010`.

**Round 2 wrote nothing under `docs/`**, which is the right disposition and not an oversight: the
two documents the corrected docstring restates were already repaired in round 1 and are already
`to-update` rows. The defect was that the source did not follow them.

## Sections restated at the ending

`not an ending` — this is an item review. `scripts/engagement-state EP-001` reports **active**:
*"1 silent round(s) recorded against a threshold of 3 … still in flight: WI-0005, WI-0006"*.
Neither `## Engagement state` section was touched by this item, and both were confirmed
byte-identical to `main` above.

## Findings

**None that block.** The first review's `F1` is fixed and was checked three ways — as a diff, as
three claims against their sources, and as a grep over the whole of `envel/` and `tests/`. Every
hunk of `main..wi/WI-0006` maps to a criterion or a plan step: `cli.py` ×4 → AC1, AC13, AC15 (plan
step 4); `dates.py` ×2 → AC2, AC5 (declared deviation 1); `envelopes.py` ×4 → AC3, AC4 (plan step
2); `store.py` ×5 → AC4 (plan step 1); `summary.py` ×9 → AC2, AC5–AC13 (plan step 3), plus this
round's comment hunk → the send-back. No hunk serves neither, and no hunk contradicts an ADR.

**F2 — observation, carried to the retrospective. Nothing in the pipeline reads source comments
for stale claims.** The first review found `F1` only by reading the diff: the invalidation set is
scoped to `docs/`, `lint-claims` walks markdown, D12 says *"every claim in `docs/`"*, and `verify`'s
ADR conformance row looked at the line **below** the docstring for the behaviour. This is F-062's
own story recurring one level outside every gate written for it. This review answered it by hand —
six source-comment claims audited above — which is a person compensating for a missing gate rather
than a gate. Recorded for `retro`; it has no owner inside this project.

**F3 — observation, no action. `overview.md`'s *"one field more"* is literally two on a described
spend**, because `description` is optional. It predates this item, which put `ref` on every kind
and so did not move the differential, and the sentence names `on` in the same breath. `implement`,
`verify` (twice) and both reviews have now read it and said so. Not a defect, and not this item's
to rewrite.

**F4 — observation, no action. `envel entries` spells a month `--month`; `envel summary` spells it
as a plain word.** `WI-0003` AC1 still holds — re-checked here, `envel summary --month 2026-08` is
refused with `usage: envel summary` and exit 2. The stakeholder's *reason* at `WI-0003/Q-004` was
*"I'd rather everything in this tool be typed the same way than have one command that's special"*,
and `refine` spent that same delegation on this deliberately, naming `envel summary` as the
alternative and pricing a disagreement at an amendment to AC1 and AC15. Not an unrecorded decision:
the sign-off at the ending must name every answer spent under delegation, so `WI-0003/Q-004` and
what was assumed under it go in front of the stakeholder by gate rather than by anyone remembering.

**F5 — observation, no action. `envelopes.take_ref` mutates the store it is handed**, and the
invariant that it is called only on the deep copy, past every refusal, lives in its docstring. All
call sites obey it and `tests/test_envelopes.py` `test_a_refused_operation_takes_no_number` guards
the refusal path for the operations that exist. `WI-0005` adds operations that append entries;
whoever writes them should read that docstring.

## Accepted gaps

The owner column is the bare answer the gate reads; the reasoning is in the gap column beside it.

| gap | owner | disposition |
|-----|-------|-------------|
| AC4's promise that a reference survives a **removal** is not observable here: no command removes an entry, so no test can distinguish a stored reference from one derived at write time. `verify` proved the limit by mutation at this head — `take_ref` returning `len(entries) + 1` produces identical output today (M1), while a constant does fail (M1b). The item that makes it observable is `WI-0005`, which adds `envel remove` and already records `depends-on: WI-0006`, so the board dispatches it the moment this item closes | WI-0005 | item-filed:WI-0005 |
| `envel fix` and `envel remove` do not exist on this branch. Not deferred work from this item: they are `WI-0005`'s own criteria, and this item delivers the reference they are aimed with | WI-0005 | item-filed:WI-0005 |
| A store this branch writes is at `format: 2` and the previous version refuses it outright — reproduced during this round's AC14 comparison, which had to be run over a format-1 store for that reason. Not deferred work: `ADR-0010` argues it as the accepted cost (*"Reversibility: hard, and it gets harder with use"*) and `ADR-0002`'s refusal path behaves exactly as designed, writing nothing | none | no-owner |
| A hand-edited `next-ref` below an existing `ref` would produce a duplicate reference, and nothing defends against it. Not deferred work: `ADR-0010` `## Consequences` declines the repair by name — *"inventing a repair now would be code no criterion asks for"* | none | no-owner |
| A month boundary across a year end was not exercised. Not deferred work: no criterion names one, and month comparison is string comparison over zero-padded ISO, so `2026-12 < 2027-01` holds by construction rather than by code | none | no-owner |
| Two invocations writing at once was not exercised. Not deferred work: concurrency is in no item's scope, and `ADR-0002`'s atomic write is the whole of what exists. This item added a **read** that does not write, which was checked | none | no-owner |
| The corrected docstring has no test and none was added. Not deferred work: there is no test for a comment. It was checked as a claim instead, three sentences against `ADR-0007`, `overview.md` and a store the tool wrote — see `## What I examined` | none | no-owner |

## Verdict

**Accepted.** Merged into `main` and closed as `delivered`.

The send-back's finding is fixed and the fix was checked as a claim rather than taken on sight.
Fifteen criteria are demonstrated by commands run at this head, twelve mutations were applied with
eleven caught and the twelfth declared, ten ADRs conform, twenty-nine invalidation entries are
disposed and the two engagement-state sections are byte-identical to `main`. The trial merge's
tests pass on the merge result and `main` did not move during it.
