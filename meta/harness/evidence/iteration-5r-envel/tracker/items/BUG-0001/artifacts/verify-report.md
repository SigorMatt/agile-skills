# Verification report — BUG-0001

Verified-commit: df2cf4d4e0c48693a996935e68119618cff801a2

Every verdict below rests on a command this execution ran against that commit, in a scratch store
addressed by `ENVEL_FILE` [src: ADR-0003], with the output quoted. The criteria were read first and
the evidence for each was derived from the criterion's own sentence; the implementation report was
read afterwards and is cited nowhere as evidence. Five scratch stores were used and each is named
in the row that used it: `/tmp/vfy1` (the bug's own steps), `/tmp/vfy2`, `/tmp/vfy4` and `/tmp/vfy5`
(the boundaries), `/tmp/vfy6` (the intersection with the older refusals).

## Verdict

**Pass.** All six acceptance criteria are met. None failed, none was ambiguous, none was
substituted. No defect of this item's own was found, and no bug item was filed — one observation
about an older criterion's wording is recorded under `## Defects found` as a finding for the ending
rather than a defect, with the reasoning for that classification.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | The bug's steps 1–4 in `/tmp/vfy1`, then `python3 -m envel entries groceries --month 2026-08`; its first and last lines piped through a `re.match(r'^-\d', word)` filter over whitespace-delimited words | `groceries held 0.00 at the start of 2026-08` / `2  2026-08-14  spend  groceries  -250.00  august shop` / `groceries was 250.00 short at the end of 2026-08`, exit 0. The filter over the two balance lines printed `negative-looking words: []` for each | No amount below zero on either balance line. The closing line says it in words, names the envelope `groceries` and the amount `250.00`, unsigned and with exactly two decimal places [src: WI-0003 AC11 "Every figure the summary prints is a plain decimal with exactly two decimal places"]. The entry line's `-250.00` is out of scope and kept its sign, as `## Expected behaviour` requires. The same wording was confirmed on a non-round magnitude (`g was 100.01 short at the end of 2026-08`, `/tmp/vfy5`) and on the **opening** line (`g was 100.01 short at the start of 2026-09`) |
| AC2 | pass | Steps 1–4 in `/tmp/vfy1` plus step 7's probe — `envelopes[0].created` set from `2026-09-11T11:29:38Z` to `2026-08-01T09:00:00Z` in the store file — then `python3 -m envel summary 2026-08` | Before the probe: `no envelopes existed in 2026-08`, exit 0 — which is why the probe is needed [src: WI-0003 AC7 "existed by the end of"]. After it: `groceries  in 0.00  spent 250.00  moved 0.00  short 250.00`, exit 0 | No column of the row carries an amount below zero. The `left` column is worded and carries `250.00` unsigned, the same way AC1's closing line does. `moved` is `0.00` in this scenario, so the criterion is decidable without reaching a transaction sign |
| AC3 | pass | Step 4 run with the two streams redirected to separate files and `$?` captured: `python3 -m envel spend groceries 250.00 "august shop" --on 2026-08-14 >s4.out 2>s4.err`; then `wc -c <s4.err`; then `python3 -m envel list` | `exit=0`; stdout `spent 250.00 from groceries, which now holds 50.00`; stderr **0 bytes**; `python3 -m envel list` → `groceries  50.00`, exit 0 | The input is not refused and the spend is recorded. Independently of the run: `git diff 127664a --stat -- envel/` is `envel/summary.py \| 62` and nothing else, so `envel/envelopes.py` and `envel/cli.py` are absent from the diff and no refusal could have been added |
| AC4 | pass | `git show 127664a:envel/summary.py > envel/summary.py`, confirmed by `git diff --stat` showing `1 file changed, 6 insertions(+), 56 deletions(-)`, then `python3 -m unittest -v tests.test_entries.AMonthThatClosedShort tests.test_summary.AMonthThatClosedShort`; then the file restored and the same command re-run | At `127664a`: `FAILED (failures=6)` of 11. The AC1 test `test_the_closing_line_says_how_short_it_was_instead_of_a_minus` **FAIL** and the AC2 test `test_the_row_says_how_short_the_month_closed` **FAIL**, the latter reading `AssertionError: 'short 250.00' not found in 'groceries  in 0.00  spent 250.00  moved 0.00  left -250.00'`. Restored: `Ran 11 tests` / `OK`, and the full suite `Ran 310 tests` / `OK` | A test reproducing steps 1–4 and asserting AC1 exists and behaves as the criterion requires, and so does a second asserting AC2. The five of the eleven that pass at `127664a` assert *unchanged* behaviour — the entry line's sign, the `moved` sign, and two months that did not close short — so passing at both commits is correct for them, and their sensitivity is checked separately under `## Test sensitivity check` |
| AC5 | pass | `git diff 127664a --stat -- tests/`; `git diff 127664a -- tests/ \| grep -c "^-[^-]"`; `git diff 127664a --name-only -- tests/`; `git diff 127664a -- tests/ \| grep -E "^\+(import\|from)"`; then each of the four modules run alone and the whole suite | `2 files changed, 124 insertions(+)` — `tests/test_entries.py \| 69 +` and `tests/test_summary.py \| 55 +`. Removed lines: **`0`**. Named files: only those two, so `tests/test_envelopes.py` and `tests/test_corrections.py` are untouched. The only non-class addition is `+import re`. Per module: `test_envelopes` 47 OK, `test_summary` 32 OK, `test_entries` 34 OK, `test_corrections` 38 OK; whole suite `Ran 310 tests` / `OK` | Additions only, in the two files AC5 allows, with no assertion existing at `127664a` edited. The guards themselves were not taken on trust — they were triggered, in a store whose past month had closed short; see `## A criterion whose subject is other criteria` |
| AC6 | pass | `summary.figures` and `summary.balance_before` / `balance_through` read directly off `/tmp/vfy1/store.json` and `/tmp/vfy5/store.json`, and the printed lines of AC1 and AC2 read against them | `/tmp/vfy1`, 2026-08: `income=0 spent=25000 moved=0 left=-25000`; `0 - 25000 + 0 == -25000` → `True`; `left` is negative, so nothing is clamped. Listing side: `balance_before=0`, entry cents `[-25000]`, `balance_through=-25000`, and `0 + (-25000) == -25000` → `True`. The printed lines name `250.00` in both places, not `0.00`. `/tmp/vfy5`, the non-round case: `left=-10001` and the line names `100.01` | The worded figure is the magnitude of the figure the arithmetic produced. The clamp AC6 exists to exclude was then *introduced deliberately* and the criterion's own tests caught it — see `## Test sensitivity check` |

All six are ticked in `item.md`.

## A criterion whose subject is other criteria

Two criteria here have criteria as their subject, and both are read rather than run
[src: toolkit: dor-dod.md "A criterion about other criteria is read against their text" "one whose subject is other criteria rather than behaviour"]. The tests are evidence for the reading, not the
reading itself.

**AC5 — "The guards that already hold still hold".** It names four test modules; the guards those
modules state are named in this item's `## Summary`, which cites them. Covered criteria, by ID:

| criterion | its sentence | verdict read against the new behaviour | what I ran |
|-----------|--------------|----------------------------------------|------------|
| `WI-0002` AC5 | *"Recording a spend larger than the amount currently in the envelope is refused … The listing never shows a negative amount for any envelope"* | **still true.** Its subject is `envel list` and the current balance, which this change does not touch; the refusal lives in `envel/envelopes.py`, absent from the diff. See `## Defects found` for the one reading of *"the listing"* under which the sentence is not literally true of the tool, and why that is not this change's doing | In `/tmp/vfy6`, whose 2026-08 had already closed short (`groceries was 250.00 short at the end of 2026-08`): `python3 -m envel spend groceries 999.00 "too much"` → `groceries holds 50.00, which is less than 999.00. Nothing has been recorded; move money into it first if you want to spend that.`, exit 1; `python3 -m envel list` → `groceries  50.00`, exit 0 |
| `WI-0005` AC9 | *"A correction that would take an envelope below zero is refused: nothing is changed, and the message names the envelope, the amount it holds and how much short of the corrected figure that leaves it"* | **still true.** Same subject — the current balance — and the same untouched module | In `/tmp/vfy6`: `python3 -m envel fix 1 --amount 10.00` → `groceries holds 50.00, and this change would leave it 240.00 short. Nothing has been changed.`, exit 1; `python3 -m envel remove 1` → `groceries holds 50.00, and removing this would leave it 250.00 short. Nothing has been removed.`, exit 1; `envel list` → `groceries  50.00` after each |
| `WI-0002` AC6, `WI-0005` AC10 | the zero-and-negative-amount refusals | **still true**, and untouched for the same reason | `tests/test_envelopes.py` 47 tests and `tests/test_corrections.py` 38 tests run green and unmodified |

**AC6 — "without either being amended".** It names two criteria explicitly:

| criterion | its sentence | verdict read against the new behaviour | what I ran |
|-----------|--------------|----------------------------------------|------------|
| `WI-0003` AC3 | *"For each envelope, money in, minus money spent, plus money moved, equals the change in that envelope's amount across the month"* | **still true.** The identity is over the figures, and the figures are unchanged signed cents. What changed is that the last one is *printed* as `short 250.00`; read as the shortfall it names, it is the same number, which is what the stakeholder settled — *"a figure I can read is what the adding-up rule was about"* [src: BUG-0001/Q-001] | On `/tmp/vfy5`, both months: 2026-08 `in - spent + moved = -10001` and `left - before = -10001 - 0`; 2026-09 `= 40000` and `29999 - (-10001)`. Both `True`. The identity was checked on the **short** month, not only on a comfortable one |
| `WI-0006` AC9 | *"the opening amount, plus the amounts on the lines between, equals the closing amount"* and *"The closing amount equals what `envel list` shows … when the month named is the month today falls in"* | **still true**, in both clauses, including when the opening amount is the worded one | `python3 -m envel entries g --month 2026-09` → `g was 100.01 short at the start of 2026-09` / `1  2026-09-11  income  g  400.00` / `g holds 299.99 at the end of 2026-09`; `-100.01 + 400.00 = 299.99`. Second clause: the same closing line against `python3 -m envel list` → `g  299.99` |

**Non-intersection, stated in those words: nothing executable exercises `WI-0002` AC5 or
`WI-0005` AC9 together with the new worded-shortfall behaviour.** `tests/test_envelopes.py` has no
2026-08 date at all (`grep -c "2026-08"` → `0`) and `tests/test_corrections.py`'s two occurrences
are a spend's date being corrected, with no assertion on a listing's balance line; no test in the
suite builds a store whose past month closed short and then triggers one of the three refusals.

I exercised that intersection myself, at the command line, in `/tmp/vfy6` — the three rows above
were all run in a store whose 2026-08 was 250.00 short — so the gap is examined rather than merely
unnoticed. **I waive the permanent covering case, by name: `WI-0002` AC5 and `WI-0005` AC9.** The
reason is structural rather than a judgement that the happy path looked convincing: the two
criteria's figure is `envelopes.balance`, the new behaviour's figure is
`summary.bounded_balance`, they are different functions in different modules, and the module the
refusals live in is absent from this branch's diff — so there is no code path by which the
rendering could reach a refusal. A test combining them could not fail for a reason connected to
this change. The case is cheap to add if a later change ever does touch `envel/envelopes.py`.

## ADR conformance

One row per ID the plan's `## Binding ADRs` section names — nine, not the five it lists as bullets: the
section's closing paragraph names `ADR-0003`, `ADR-0007`, `ADR-0010` and `ADR-0011` in the course of
explaining that they do **not** constrain this change, and the gate reads every ADR token in the
section as binding. Those four therefore get `not-engaged` verdicts below, which is the same claim the
plan was making in prose. No ADR outside the nine was found engaged.

| ADR | verdict | clause quoted from its Decision | file and line, or why not engaged |
|-----|---------|---------------------------------|-----------------------------------|
| `ADR-0001` | conforms | *"Two functions in `envel/money.py` are the only places the two forms meet … No other module converts between them, and no amount is ever held as a `float` or written to the store as a decimal string."* | Both new helpers hand cents to the formatter and concatenate words around the result: `envel/summary.py:82` (`"short {}".format(money.format_amount(-cents))`) and `envel/summary.py:238` (`money.format_amount(-cents)` inside the worded sentence). Checked for a bypass across the package, not only in what was written: `grep -rn "parse_amount\|:\.2f\|/ 100\|// 100\|% 100" envel/ --include=*.py` → `money.py:20`, `money.py:42`, and four `parse_amount` **calls** in `cli.py` at 161, 167, 176, 183. No third conversion site |
| `ADR-0002` | conforms | *"`entries` is ordered as written, and an envelope's balance is the sum of `cents` over the entries naming it — the second half with no branch on `kind`"* and *"Every amount in the file is a whole number of cents"* | Nothing is stored, cached or clamped: `git diff 127664a --stat -- envel/` is `envel/summary.py` alone, so `envel/store.py` is absent from the diff, and the `format` field is unread by this change. `bounded_balance` at `envel/summary.py:196` is still the plain `sum(entry["cents"] …)` with no branch on `kind`. The store file written by the AC3 run was read back as JSON and its `cents` are integers (`-25000`) |
| `ADR-0008` | conforms | Decision 3's table, the `left` row: *"left \| month <= M \| `cents`"*; and Decision 4: *"Nothing is precomputed and nothing new is stored"* | `figures()` at `envel/summary.py:49` is not in the diff's changed hunks and still ends `return income, spent, moved, left`; `balance_through` at `envel/summary.py:218` is still `bounded_balance(store, name, lambda falls_in: falls_in <= month)`. The `## Consequences` identity was checked as arithmetic on the short month: `left − (in − spent + moved)` = `0` = `balance_before` for 2026-08 and `-10001` = `balance_before` for 2026-09, so nothing derives the carried-in figure by subtraction |
| `ADR-0009` | conforms | *"`summary` prints nothing and calls no `sys.exit`"* | `grep -n "print(\|sys\.exit\|import sys" envel/summary.py` → **no hit at all**. Each new helper is a single `return` of a `format()` expression: `envel/summary.py:81-83` and `envel/summary.py:236-242`. Both are called from `row()` and `list_entries()`, which still return through `envelopes.Ok`; `envel/cli.py` is absent from the diff, so no dispatch shape changed |
| `ADR-0012` | conforms | Decision 1: *"`figures()`, `bounded_balance()`, `balance_before()` and `balance_through()` are unchanged, and keep returning signed cents"*; Decision 2's two helper signatures and their two sentences; Decision 4: *"Transaction figures keep their signs"*; Decision 5: *"The current-balance messages are untouched"* | Decision 1 — `figures` returns `left=-25000` for the short month, read directly. Decision 2 — `left_column` at `envel/summary.py:72` and `balance_line` at `envel/summary.py:222`, and the delivered strings are the ADR's own, verbatim: `groceries was 250.00 short at the end of 2026-08` and `groceries  in 0.00  spent 250.00  moved 0.00  short 250.00`. Decision 3 — as `ADR-0001` above. Decision 4 — the entry line still reads `-250.00` and the `moved` column still reads `-100.00` for an envelope that only gave money away (`/tmp/vfy4`: `source  in 0.00  spent 0.00  moved -100.00  short 100.00`). Decision 5 — `envel list` printed `groceries  50.00` through every run, and the success clause `spent 250.00 from groceries, which now holds 50.00` is unchanged |

| `ADR-0003` | not-engaged | *"The store path is, in order: 1. `$ENVEL_FILE`, used exactly as given, if it is set and non-empty"* | Not engaged: this change reads no path and opens no file. `envel/store.py` and `envel/cli.py` are both absent from `git diff 127664a --name-only -- envel/`, whose only entry is `envel/summary.py`. The ADR is load-bearing for *how this report was produced* — every command above ran against a scratch store via `ENVEL_FILE` — but nothing in the change is constrained by it |
| `ADR-0007` | not-engaged | *"A move appends exactly two entries to `entries`"*, and *"`cents` carries the direction, negative on the side the money left"* | Not engaged: nothing here appends, reads or branches on a `move` entry. The change renders a balance that a move's `cents` contributes to like any other entry's, with no branch on `kind` — `bounded_balance` at `envel/summary.py:196` is unchanged. Its second clause is *adjacent*, because the `moved` column's sign follows from it, and that column is out of scope and unchanged; I confirmed the sign survives (`source  …  moved -100.00`, `/tmp/vfy4`) rather than assuming it |
| `ADR-0010` | not-engaged | *"An entry carries `ref`, a positive integer, written when the entry is appended and never changed afterwards"*, and *"`store.FORMAT` becomes `2`"* | Not engaged: no reference is issued, read for meaning, or renumbered, and `format` is neither read nor written. The refs printed on the entry lines above (`1`, `2`, `3`, `4`) come from `entry_line`, which this change does not touch. `envel/store.py` is absent from the diff |
| `ADR-0011` | not-engaged | *"A correction **mutates the entry** identified by `ref` … A removal **deletes that entry** from the list"*, and Decision 5's *"refuse if either is negative"* | Not engaged as a constraint on the design — the plan says so, and the reason is that no step touches `envel/envelopes.py`, where both operations live, and it is absent from the diff. Its below-zero refusal is the **neighbouring** rule rather than a constraint, so I reopened it as an invalidation-set entry instead of taking the diff's silence for an answer: both refusals were triggered in `/tmp/vfy6` and both held, quoted above |

## Invalidation set

One row per entry in the plan's set. I wrote no document: `git diff main...wi/BUG-0001 --name-only -- docs/`
prints nothing, and this execution made no edit under `docs/` either.

| document | disposition | what I reopened, and what I found |
|----------|-------------|-----------------------------------|
| `docs/product/vision.md` — the v8 paragraph *"`envel entries` and `envel summary` say how short the month closed, in words, rather than printing a negative"* | `verified-still-true` — **confirmed** | Read at `docs/product/vision.md:73` against the branch head. The claim is that the two commands say it in words rather than printing a negative, and both do: `groceries was 250.00 short at the end of 2026-08` and `short 250.00`. One thing I checked rather than passed over: the paragraph's quotation reads *"'Groceries was 250.00 short…'"* with a capital G, while the tool prints `groceries` lower-case. That is inside a quotation of the stakeholder's own sentence at [src: BUG-0001/Q-001], not a claim about the tool's output, and the envelope's name is printed as it was typed [src: WI-0001 AC12 "The listing shows an envelope's name exactly as it was typed"]. Not a discrepancy |
| `docs/product/vision.md` — *"A correction that would take an envelope below zero is refused and says how short the envelope is"* | `verified-still-true` — **confirmed** | Read at `docs/product/vision.md:48`. Reopened by triggering it rather than by reasoning about the diff: in `/tmp/vfy6`, `fix` and `remove` both refused and both named how short. Its subject is the current balance, which this change does not reach |
| `docs/product/vision.md` — `## Engagement state`, all four bullets | `owned-by-ending` | Left exactly as it is. Not read for repair, not edited, and not edited by this item: no `docs/` file is in the branch's diff |
| `docs/architecture/overview.md` — *"Amounts are printed with exactly two decimal places and no currency symbol"* | `verified-still-true` — **confirmed, and checked with a falsifier that could have fired** | Read at `docs/architecture/overview.md:93`. **Set:** every place in `envel/` where cents become printed text. **Enumerated by:** `grep -n "format_amount" envel/summary.py` → 8 call sites, at lines 82, 83, 101, 102, 103, 171, 238, 241, the two new ones among them; and `grep -rn "parse_amount\|:\.2f\|/ 100\|// 100\|% 100" envel/ --include=*.py` → no conversion outside `money.py`. **Verdict:** true of each. **Falsifier:** a member that builds the string itself, which would most plausibly show as a dropped trailing zero. I chose the boundary over the happy path deliberately and ran a **non-round** magnitude: `/tmp/vfy5` printed `g was 100.01 short at the end of 2026-08` and `spent 100.01`, and a whole magnitude printed `250.00` rather than `250.0`. A hand-rolled `str(-cents / 100)` would have produced `100.01` *and* `250.0`, so the case could have failed and did not |
| `docs/architecture/overview.md` — *"the only two places text and amounts meet: parse and format"* | `verified-still-true` — **confirmed** | Read at `docs/architecture/overview.md:33`. **Set:** every function in `envel/` converting between an amount and text. **Enumerated by:** the second grep above. **Members:** `money.parse_amount` at `money.py:20` and `money.format_amount` at `money.py:42`, and no third. **Verdict:** true — the two new helpers produce text *containing* an amount without converting one, each delegating to the formatter. **Falsifier:** a `cents // 100` outside `money.py`; the grep is over the whole package and `summary.py` is exactly where one would have appeared, since both helpers handle a sign |
| `docs/architecture/overview.md` — the `envel/summary.py` row, *"the reports, both of them"* | `verified-still-true` — **confirmed** | Read at `docs/architecture/overview.md:31`. The module still owns two reports and gained no third: `summarise()` and `list_entries()` are the only functions in it taking a `store` and a `month` and returning through `envelopes.Ok`/`Refusal`, and `envel/cli.py` is absent from the diff, so nothing new is dispatchable. `left_column` and `balance_line` take no `store` and are called only from those two |
| `docs/architecture/overview.md` — `## What is not decided yet` | `to-update`, **discharged by `plan`** | Verified rather than assumed: the section now names `BUG-0001` and `ADR-0012` as the last design taken; the document is at `version: 10`; and the change-log row for v10 exists, stamped `2026-09-11T11:13:17Z` with actor `plan` and item `BUG-0001`. `git show 51a0a62 --stat -- docs/` shows the repair landed on `main`, not on this branch |
| `docs/architecture/overview.md` — `## Engagement state` | `owned-by-ending` | Left as it is. Independently checked that `plan`'s v10 edit did not reach it: `git show 51a0a62 -- docs/architecture/overview.md` adds only the v10 change-log row and the `## What is not decided yet` rewrite, and no line of `## Engagement state` appears in the diff |
| `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md` — Decision 3's filter table (`left` row) and `## Consequences` first paragraph | `verified-still-true` — **confirmed** | Reopened as arithmetic on the short month rather than as a read. The table's `left` row still describes `figures()`, and `## Consequences`' *"nothing **derives** the carried-in figure from the other three"* was checked by computing `left − (in − spent + moved)` and comparing it with `balance_before` for both months of `/tmp/vfy5`: equal in both, including where the carried-in figure is itself negative (`-10001`) |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` — `## Consequences`, *"a module that prints an amount without going through"* the formatter | `verified-still-true` — **confirmed** | Same set, enumeration and falsifier as the `## Conventions` row above, including the non-round-magnitude case that could have fired. Read at `ADR-0001-amounts-are-integer-cents.md:58` |
| `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` — `## Consequences`, *"`summary` prints nothing and calls no `sys.exit`"* | `verified-still-true` — **confirmed, on a stronger grep than the one claimed** | **Set:** every statement in `envel/summary.py`. **Enumerated by:** `grep -n "print(\|sys\.exit\|import sys" envel/summary.py` → **no hit**. The implementation report's grep was on the bare word `print`, which matched four docstring prose hits; searching for the call form `print(` leaves nothing at all, which is the stronger result and the same verdict. **Falsifier:** a `print(` or an `import sys` in the module — and the two new functions are where one would have been, since both exist to produce user-visible text |
| `docs/architecture/adr/ADR-0011-a-correction-edits-the-entry-in-place.md` — Decision 3/5, the below-zero refusal on `fix` and `remove` | `verified-still-true` — **confirmed** | Reopened by triggering both refusals in `/tmp/vfy6`, quoted under `## A criterion whose subject is other criteria`, not by observing that `envel/envelopes.py` is absent from the diff — though it is |

No entry was left open, no entry disposed `owned-by-ending` was touched, and no document was
repaired by this execution.

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → `Ran 310 tests` / `OK`, exit 0, run twice against the branch head: once at the start and once after the mutations below were reverted |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | pass | `python3 .claude/agile-skills/scripts/validate-workspace .` → `checked 8 item(s), 14 document(s)` / `0 errors, 0 warnings`, exit 0 |
| `every-criterion-independently-checked` | pass | Six rows in `## Criteria`, each naming the command this execution ran and quoting its real output. No row cites `impl-report.md` |
| `negative-cases-exercised` | pass | See `## Negative and boundary cases exercised` — nine conditions triggered, including the `cents < 0` branch boundary from both sides |
| `a-criterion-about-criteria-is-read` | pass | `## A criterion whose subject is other criteria` — AC5 and AC6, five covered criteria named by ID with a per-criterion verdict read from their text, the non-intersection stated in those words, and the covering case waived by name with a structural reason |
| `adr-conformance-is-decided` | pass | `python3 .claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item BUG-0001` → exit 0. Five rows in `## ADR conformance`, each quoting a clause of the ADR's `## Decision` |
| `invalidation-set-is-disposed` | pass | `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item BUG-0001` → exit 0. Twelve rows in `## Invalidation set`; the nine claiming a document still true were reopened and read against the branch head |
| `tests-would-fail-without-the-change` | pass (advisory) | `## Test sensitivity check` — four mutations, each confirmed present on disk by `grep` before the tests were run |

## Negative and boundary cases exercised

The branch in both helpers is `cents < 0`, so zero is the boundary and it is checked from both
sides.

1. **A past month closing exactly `0.00`** — the boundary itself, reached from the command line in
   `/tmp/vfy4` by dating a `move` into the month (`envel move` takes `--on`) and spending exactly
   it: `python3 -m envel move source target 100.00 --on 2026-08-05` then
   `python3 -m envel spend target 100.00 "spent exactly it" --on 2026-08-20`. The listing closed
   `target holds 0.00 at the end of 2026-08` and the row read `target  …  left 0.00` — **not**
   `short 0.00`. Zero takes the unworded branch, which is what the criteria require.
2. **A past month one cent below the boundary** — `/tmp/vfy5`, a `100.01` spend backdated against
   `400.00` of income: `g was 100.01 short at the end of 2026-08`, and the row `short 100.01`.
3. **A negative *opening* line** — the month after a short month, `/tmp/vfy5`:
   `g was 100.01 short at the start of 2026-09`. The plan recorded this wording as its own
   assumption rather than the stakeholder's; it is what was delivered.
4. **A month with nothing recorded for the envelope** — `python3 -m envel entries g --month 2026-07`
   → `g held 0.00 at the start of 2026-07` / `nothing was recorded against g in 2026-07` /
   `g holds 0.00 at the end of 2026-07`, exit 0. Unchanged, and the middle line is not worded.
5. **A month with no envelope in it** — `python3 -m envel summary 2026-08` before step 7's probe →
   `no envelopes existed in 2026-08`, exit 0 [src: WI-0003 AC4 "A month for which there is no row to print"].
6. **A month that did not close short** — `g  in 400.00  spent 0.00  moved 0.00  left 299.99`, the
   old wording exactly.
7. **The overspend refusal, inside a short-month store** — `/tmp/vfy6`:
   `python3 -m envel spend groceries 999.00 "too much"` → exit 1, the message naming what is left,
   `envel list` still `groceries  50.00`.
8. **The below-zero refusals on `fix` and `remove`, inside a short-month store** — `/tmp/vfy6`,
   both exit 1, both naming how short, the listing unchanged after each.
9. **A negative transaction figure beside a worded balance in the same row** — `/tmp/vfy4`:
   `source  in 0.00  spent 0.00  moved -100.00  short 100.00`. Both conventions in one line, which
   is the distinction `ADR-0012` Decision 4 draws. Recorded as a finding below.

One further negative case was attempted and could not be constructed: a spend of `100.01` against
`100.00` of income was refused outright (`onecent holds 100.00, which is less than 100.01`), because
the **current** balance guard fires first. The one-cent case was reached instead by giving the
envelope more income, which is case 2 above.

## Test sensitivity check

Four mutations, each applied to the working tree, each **confirmed on disk by `grep` before the
tests were run**, and each reverted by restoring the file from a copy of the branch head taken
first. `git status --porcelain` was empty after every revert and after the last.

| mutation | what it removes | result |
|----------|-----------------|--------|
| `envel/summary.py` replaced wholesale with `git show 127664a:envel/summary.py` | the whole fix | `FAILED (failures=6)` of 11 in the two new classes, the AC1 and AC2 tests among them |
| `return income, spent, moved, max(0, left)` in `figures()` | clamps the summary's arithmetic — **AC6's falsifier** | `test_the_arithmetic_was_not_clamped` **FAILS**. The companion entries-side test passes, correctly: it reads `balance_before`/`balance_through`, which do not go through `figures()` |
| `return max(0, sum(…))` in `bounded_balance()` | clamps the listing's arithmetic — AC6's falsifier on the other side | `FAILED (failures=3)` of the 6 in `tests.test_entries.AMonthThatClosedShort` |
| `money.format_amount(abs(moved))` in `row()` | the `moved` column's sign, which `ADR-0012` Decision 4 keeps | `test_the_moved_column_keeps_its_sign` **FAILS** |
| `money.format_amount(abs(entry["cents"]))` in `entry_line()` | the entry line's sign, which this bug leaves in scope of nothing | `FAILED (failures=6)` across `tests.test_entries` |

Honest note on method: the `abs(moved)` mutation was run once *without* a confirming `grep` first
and the suite came back green, which would have been a finding about an insensitive test. Re-run
with the edit confirmed present at `envel/summary.py:103`, the guard test fails. The first run is
recorded as void — I cannot show the edit was on disk when those tests ran — and every mutation in
the table above was grep-confirmed before its run. That is why the confirmation step is in the
method and not merely in the intent.

No test was found that passes against code with the behaviour it claims to test removed.

## Defects found

**None of this item's own criteria failed, and no bug item was filed.** One observation is recorded
here because it belongs in front of the ending rather than in a journal nobody re-reads.

**`WI-0002` AC5's sentence is not literally true of the tool, under one reading of *"the
listing"*.** The sentence is *"The listing never shows a negative amount for any envelope"*, and
`envel entries` — a listing — shows `-250.00` on an entry line, as case 9 above shows it showing
`moved -100.00` in a summary row. I classify this as a finding and **not** a defect, on three
grounds, and I record the grounds because the classification is the part worth checking:

1. **It is not this change's doing.** Entry lines carried signs before this branch existed, and the
   branch's only behavioural change is to two balance lines and one column. The mutation table
   above shows the sign-keeping is asserted by tests that predate it.
2. **`WI-0002` AC5's subject is `envel list`.** `envel entries` did not exist when it was written —
   it came with `WI-0006` — and this bug's own `## Summary` reads the sentence that way when it
   cites it.
3. **The stakeholder has already been asked and has already answered.** The entry line
   `2  2026-08-14  spend  groceries  -250.00  august shop` was printed verbatim in the context they
   read at [src: BUG-0001/Q-001], and the option they chose left it alone; this item's
   `## Expected behaviour` and AC5 then put it out of scope deliberately. Re-asking would be
   re-opening a settled decision, so I have filed no question.

What the ending should weigh is narrower than the sentence: `EP-001`'s success measure is *"No
envelope ever shows a negative amount"*, and after this change a reader of `envel summary` can
still see a minus in the `moved` column. That is a transaction figure by `ADR-0012`'s distinction
and by [src: WI-0003 AC2 "The moved figure is one net number, positive when more arrived than left"],
which the stakeholder approved — but the measure's wording does not carry the distinction, and
whoever closes `EP-001` should say so explicitly rather than let the measure read as unqualified.
No item's criteria require a change here, which is why this is a finding and not a send-back.

## Not verified, and why

- **The stakeholder's approval of the two wordings this change invented.** They approved
  `groceries was 250.00 short at the end of 2026-08` [src: BUG-0001/Q-001]. They were never shown
  `short 250.00` for the summary column, nor `was … short at the start of` for an opening line; the
  plan records both as its own assumptions, *not under delegation*. I verified the delivered strings
  are the ones the plan and `ADR-0012` specify. Whether they are the ones the stakeholder wants is
  not a question any command here can settle, and the plan's own `## Risks` says it will surface
  only at the ending. It is in front of the ending now, in this section.
- **That the rule holds for reports that do not yet exist.** `ADR-0012`'s obligation is on three
  call sites, and nothing enforces it: a future report printing a bounded balance without calling
  `balance_line` or `left_column` would reintroduce this bug and no check in the suite would fail.
  I confirmed the three existing call sites, which is all there is to confirm today. `ADR-0012`
  `## Risks` names this and nothing was added to enforce it.
- **The step-7 probe is a hand edit of the store file, not a state the tool can reach.** AC2 names
  it, so verifying AC2 means making it; `envel new` stamps `created` to now and no command backdates
  it. The store file is *"readable and repairable in any text editor"* [src: ADR-0002] and the same
  seeding is used by `tests/test_cli.py`, so the probe is legitimate — but the AC2 row below the
  probe is a verdict about a store assembled by hand, and that is worth saying plainly.
- **Multi-month and multi-envelope combinations beyond those listed.** I exercised one and two
  envelopes over three months. I did not attempt an exhaustive sweep of months, and nothing in the
  criteria asks for one.
- **Nothing was checked on a second machine, a second Python, or across a restart.** No criterion
  names any of those, so no criterion is `substituted`; this is stated so the gap is not read as a
  clean pass on ground nobody walked.
