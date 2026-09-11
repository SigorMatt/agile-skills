# Verification report — WI-0006

Verified-commit: 226ceb589166acd9ff8dc438c5b6b1e0cd6ad47d

## Verdict

**Pass**, at the second time of asking. `review-close` rejected this item on one finding — a
docstring in `envel/summary.py` that shipped the claim this same item had recorded as false in
`ADR-0007` — and `implement` fixed it. This report is the **re-verification at the new branch
head**, and it is not a re-reading of the previous one: all fifteen criteria were demonstrated again
by commands run here, twelve mutations were applied to the source and the tests watched, and the ten
binding ADRs and twenty-nine invalidation entries were decided again.

The send-back's own subject was checked first and directly: `envel/summary.py` `entry_kind` no
longer contains the sentence `ADR-0007` struck, and what it says now is each claim's own wording
from `ADR-0007` `## Decision` and `docs/architecture/overview.md` `## The data`, checked against a
store the tool wrote.

Three things a reader should carry forward, none of them a criterion failure, all in
`## Observations`: a store this branch writes cannot be read by the previous version (reproduced
here); AC4's promise about a **removal** is not observable until `WI-0005` exists; and
`envel entries` spells a month `--month` where `envel summary` spells it as a plain word.

No defect was found and no bug item was filed.

Every store below was a scratch file under `ENVEL_FILE`; no real store was touched.

### What changed since the previous verification

```
$ git diff 00b2b31..226ceb5 --stat -- envel/ tests/ bin/
 envel/summary.py | 8 +++++---
 1 file changed, 5 insertions(+), 3 deletions(-)
```

One hunk, entirely inside `entry_kind`'s docstring. That is the fact that makes this a
re-verification rather than a fresh one — but it is **evidence**, not a licence, and every table
below was produced by running something at this head.

## Criteria

All fifteen against one scratch store built with `envel new/add/spend/move`, seeded so that August
2026 and September 2026 both have entries and three envelopes exist.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | `envel entries`; `envel entries groceries`; `envel entries groceries --month 2026-08`; `envel entries --month 2026-08` | all four exit 0. Bare → 4 lines across three envelopes; `groceries` → its lines bracketed; `groceries --month 2026-08` → 3 entry lines bracketed; `--month 2026-08` → 5 lines across three envelopes | the four forms the criterion names, one invocation each. The month is `YYYY-MM`, as `envel summary` spells one |
| AC2 | pass | `envel entries --month 2026-08` on a store holding income, a described spend, an undescribed spend and a move | `8  2026-08-14  spend  groceries  -34.99  shoes on the statement` and `2  2026-08-20  spend  groceries  -12.50` | ref, date, kind, envelope, amount on every line; the description present on one and absent in the same position on the other. `-100.00` and `20.00` are two decimals, no symbol, no separator |
| AC3 | pass | recorded into three envelopes, then read the store file back | refs `1 groceries income, 2 groceries spend, 3 fun income, 4 groceries move, 5 fun move, 6 fun spend, 7 car income, 8 groceries spend, 9 car spend`; `next-ref: 10` | `fun`'s first entry is **3** and `car`'s is **7**, not 1 — counted once across everything, not within an envelope. All nine distinct |
| AC4 | pass | listed August; then `envel add groceries 7` and `envel spend groceries 3 --on 2026-08-05`; listed August again and diffed the previously-printed lines | `UNCHANGED` — refs 8, 9, 2, 4, 5 each name the same entry, character for character. The two new entries took **10** and **11**, which no earlier line had | the observable half. The removal half is not observable yet — see `## Not verified, and why` |
| AC5 | pass | `envel entries --month 2026-08` and `envel entries` over a store with dated spends, a dated move and undated income | spends and the move print under their `on` (`2026-08-14`, `2026-08-20`, `2026-08-28`) while the three incomes print under `2026-09-11`, the day they were typed | the asymmetry the criterion names. Confirmed against the store: the income entries carry no `on` at all |
| AC6 | pass | `envel entries --month 2026-08`; `envel entries groceries --month 2026-08`; `envel entries fun --month 2026-08` | with none named: `4  2026-08-28  moved out  groceries  -20.00` and `5  2026-08-28  moved in  fun  20.00` — same date, same amount, opposite directions. With `groceries`: only line 4. With `fun`: only line 5 | |
| AC7 | pass | `envel entries` (no month); `envel entries --month 2026-08` twice, diffed | bare listed only September's four entries; the two August runs were `IDENTICAL` | a past month lists the same entries whenever it is run |
| AC8 | pass | `envel entries --month 2026-08` over two entries sharing `2026-08-14`, recorded in a known order | `8  2026-08-14 … groceries` then `9  2026-08-14 … car` then `2  2026-08-20`, `4  2026-08-28`, `5  2026-08-28` | oldest first; the `08-14` tie is broken by the order the store holds them (8 before 9), and the `08-28` tie likewise (4 before 5). Two runs identical |
| AC9 | pass | `envel entries groceries --month 2026-08`; then `envel entries groceries` and `envel list` | `groceries held 0.00 at the start of 2026-08` … `-34.99`, `-12.50`, `-20.00` … `groceries holds -67.49 at the end of 2026-08`. 0.00 − 34.99 − 12.50 − 20.00 = **−67.49** | second half: the current-month listing closed `groceries holds 232.51 at the end of 2026-09` and `envel list` printed `groceries  232.51` on the same store |
| AC10 | pass | `envel entries --month 2026-08` | 5 lines, every one an entry line naming `groceries`, `car` or `fun`; **no** opening and **no** closing line | |
| AC11 | pass | `envel entries car --month 2026-07`; `envel entries --month 2026-07` | `car held 0.00 at the start of 2026-07 / nothing was recorded against car in 2026-07 / car holds 0.00 at the end of 2026-07`, stderr empty, exit **0**. With no envelope: `nothing was recorded in 2026-07`, exit **0** | a success and not a refusal; the brackets are still printed when an envelope is named |
| AC12 | pass | `envel entries nosuch`; `envel entries GROCERIES --month 2026-08` | stdout **empty**, stderr `there is no envelope called 'nosuch'. Nothing has been listed.`, exit **1**. `GROCERIES` printed the same five lines as `groceries`, exit 0 | distinguishable from AC11 by the stream and the exit code alone: AC11 is stdout/0, this is stderr/1. The message names what was typed |
| AC13 | pass | `envel entries --month` each of `2027-03`, `2026-8`, `august`, `2026-13`, `2026-08-01` | all five: stdout **empty**, exit **1**. `2027-03` → `2027-03 has not happened yet, so there is nothing to list. The month this one is in is 2026-09.`; the other four → `'…' is not a month: write it as YYYY-MM, such as 2026-08` | both cases the criterion names, each triggered. `--month 2026-09`, the month today falls in, is not refused |
| AC14 | pass | see `## AC14 — the read` below | `envel summary` and `envel list` byte-identical on `main` and on this branch across **nine** invocations over one format-1 store, with the store file's md5 unchanged by both; no listing line carries a `left ` column (`cat -A`) | read as well as run |
| AC15 | pass | the refusals at AC12 and AC13 and the successes at AC1, AC9, AC10 and AC11, one invocation each; plus `envel entries groceries extra`, `envel entries --month`, `envel entries --for 2026-08` | every refusal: stdout empty, stderr non-empty, exit non-zero. Every success: stdout non-empty, stderr empty, exit 0. All three wrong shapes printed `usage: envel entries [-h] [--month YYYY-MM] [name]` to stderr with exit **2** and nothing on stdout | the usage printed is this subcommand's, not the tool's |

## AC14 — the read

AC14 has criteria as its subject — *"`WI-0003`'s AC1 through AC14 are re-read against this item's
behaviour"* — so it is read, and the tests are evidence for the reading rather than its definition.

**The run, first.** `main` cannot read a store this branch has written (format 2), so the
comparison was made the only way it can be made: a **format-1** store built with `main`'s own
binary, then read by each side in turn from a pristine copy.

```
IDENTICAL  envel summary            (exit 0, store unchanged by both)
IDENTICAL  envel summary 2026-08    (exit 0, store unchanged by both)
IDENTICAL  envel summary 2026-09    (exit 0, store unchanged by both)
IDENTICAL  envel summary 2026-07    (exit 0, store unchanged by both)
IDENTICAL  envel summary 2027-03    (exit 1, store unchanged by both)
IDENTICAL  envel summary 2026-8     (exit 1, store unchanged by both)
IDENTICAL  envel summary august     (exit 1, store unchanged by both)
IDENTICAL  envel summary 2026-08-01 (exit 1, store unchanged by both)
IDENTICAL  envel list               (exit 0, store unchanged by both)
```

Stdout, stderr, exit code **and the md5 of the store file** matched on all nine. The store-file
check is the one that matters for a format-1 document: the branch upgrades it in memory when it
reads it, and if it also wrote, a read-only command would have rewritten the stakeholder's file.

**The read, per criterion.** `WI-0003`'s fourteen criteria, each against this item's behaviour.

| WI-0003 | still true? | read against this item |
|---------|-------------|------------------------|
| AC1 — `envel summary`, month as a plain word, `--month` refused | **yes** | `envel summary --month 2026-08` → `usage: envel summary [-h] [YYYY-MM]`, exit 2, run here. `envel entries` takes `--month`, which is a different subcommand's grammar and changes nothing about this sentence |
| AC2 — one row per envelope, four figures, a move only in the third | **yes** | the nine identical invocations include `summary 2026-08` and `summary 2026-09` over a store containing a move; the rows are unchanged from `main` |
| AC3 — the figures reconcile | **yes** | byte-identical output means the arithmetic is unchanged. Independently: `test_one_store_listed_and_then_summarised_gives_both_answers` asserts `left 60.00` in the summary and `groceries holds 60.00 at the end of 2026-08` in the listing over one store |
| AC4 — a month with no row prints a line and exits 0 | **yes** | `envel summary 2026-07` → `no envelopes existed in 2026-07`, exit 0, identical on both sides |
| AC5 — bare summary is this month; a past month is reachable | **yes** | `envel summary` and `envel summary 2026-08` both identical on both sides |
| AC6 — no total line, no individual spends | **yes** | this is the sentence AC14 exists to protect. `envel summary 2026-08` prints only the four-figure rows; the listing of individual entries is a **different command**, and `test_the_summary_lists_no_individual_entry_and_has_no_running_balance` asserts the row shape by regex |
| AC7 — a row for every envelope existing by the end of the month | **yes** | identical output over a store with three envelopes, including `summary 2026-08` where none existed yet (`no envelopes existed in 2026-08`) |
| AC8 — income falls in the month it was typed | **yes** | the same rule this item's AC5 applies to a line; `entry_month` is one expression used by both reports, and the summary's output is unchanged |
| AC9 — a later month is refused | **yes** | `envel summary 2027-03` → exit 1, identical on both sides |
| AC10 — rows ordered alphabetically, ignoring case | **yes** | identical output; `car`, `fun`, `groceries` in that order on both sides |
| AC11 — every figure two decimals, no symbol | **yes** | identical output; this item's own amounts go through the same `money.format_amount` (ADR-0001 row below) |
| AC12 — an unreadable month is refused | **yes** | `2026-8`, `august`, `2026-08-01` → exit 1, identical on both sides |
| AC13 — refusals to stderr non-zero, successes to stdout zero | **yes** | the nine invocations above compared stderr and the exit code as well as stdout |
| AC14 — a wrong-shaped command line prints the subcommand's usage | **yes** | `envel summary --month 2026-08` and `envel summary 2026-08 extra` both → `usage: envel summary [-h] [YYYY-MM]` on stderr, exit 2, nothing on stdout, run here |

**Non-intersection: there is none to state.** `tests/test_cli.py`
`test_one_store_listed_and_then_summarised_gives_both_answers` runs `envel entries` and
`envel summary` over one store in one test and asserts the summary's stdout line-for-line against
what `WI-0003` delivered. So the case covering both was **added**, not waived. `tests/test_summary.py`
is untouched by this branch — `git diff --stat main..HEAD -- tests/test_summary.py` is **empty** —
and its 27 tests pass unmodified (`python3 -m unittest tests.test_summary` → `Ran 27 tests … OK`).

## ADR conformance

Ten binding ADRs, ten verdicts. Each clause is quoted from that ADR's `## Decision`. The
enumerations behind ADR-0001, ADR-0003, ADR-0004, ADR-0005, ADR-0008 and ADR-0009 were **re-run at
this head** and are reported in `## Negative and boundary cases exercised` and below; the file and
line references were re-read against the current source.

| ADR | verdict | clause quoted from its Decision | file and line, or why not engaged |
|-----|---------|--------------------------------|-----------------------------------|
| ADR-0001 | conforms | *"Two functions in `envel/money.py` are the only places the two forms meet … No other module converts between them"* | every amount the listing prints is a `money.format_amount` call: `envel/summary.py:148` (the entry line), `:235` and `:248` (AC9's two bracket figures). **Falsifier:** a conversion written elsewhere. `grep -rn "100\b\|Decimal\|round(" envel/ --include=*.py` outside `envel/money.py` → **exit 1, no output** |
| ADR-0002 | conforms | *"`entries` is append-only within a run and ordered as written. An envelope's balance is the sum of `cents` over the entries naming it"*, and *"`format` is an integer this tool checks on load"* | `envel/summary.py:164` builds a **new** list and `:170` returns `sorted(...)`; the stored list is never reordered or mutated. `envel/summary.py:182` (`bounded_balance`) sums `cents` with a month bound; `grep "kind"` over `bounded_balance`, `balance_before` and `balance_through` → **no matches**, so no branch on the kind. The format check is `envel/store.py:83`, against `READABLE = (1, 2)`. **Boundary:** a format-1 store was listed twice and its md5 was unchanged by both runs |
| ADR-0003 | conforms | *"One function in `envel/store.py` resolves the path and nothing else knows about it"* | that function is `envel/store.py:24`. The code this item added there, `upgraded`, takes a **document** and not a path. **Falsifier:** path knowledge outside that module. `grep -rn "ENVEL_FILE\|XDG_DATA_HOME\|\.local\|pathlib\|expanduser" envel/ --include=*.py` outside `envel/store.py` → **exit 1, no output** |
| ADR-0004 | conforms | *"there are two ways to start it, both reaching the same `main`"* | that `main` is `envel/cli.py:103`; the new subcommand is registered at `envel/cli.py:86` and dispatched at `:140`, both **inside** it. Neither entry point was edited. Run at this head: `python3 bin/envel entries groceries --month 2026-08` and `python3 -m envel entries groceries --month 2026-08` → stdout md5 `0be164c3e8e5c3ec7d392c570292c658` on **both** |
| ADR-0005 | conforms | *"`commands.test`: `python3 -m unittest discover -s tests -t .`"*, *"`commands.lint`: `python3 -m compileall -q envel tests`"*, standard library only | **Enumeration, mine:** every `import` in `envel/*.py` and `tests/*.py` → `argparse, copy, dataclasses, datetime, json, os, pathlib, re, subprocess, sys, tempfile, unittest` plus the project's own `dates, envelopes, money, store, summary, main`. **Falsifier:** a name outside the standard library. There is none. The file this item adds, `tests/test_entries.py:13`-`:16`, imports `copy`, `unittest` and `envel`, and `git diff main..HEAD -- envel/ | grep -E '^[+-](import|from)'` → **exit 1**, so this branch added and removed no import anywhere under `envel/`. Both commands run here: exit 0 with 231 tests, and exit 0 |
| ADR-0006 | conforms | *"`on` is present on every spend entry … It is never absent and never null, so a reader never has to fall back to `at`"* | **Enumeration, mine:** `grep -n '"kind": "spend"' envel/envelopes.py` → exactly one site, `envel/envelopes.py:168`, and `envel/envelopes.py:171` writes `"on"` unconditionally from the argument. **Boundary:** a spend recorded on 2026-09-11 but dated `--on 2026-08-14` listed under **2026-08-14**, in August and not in September |
| ADR-0007 | conforms | *"A move appends exactly two entries to `entries`"*, *"`cents` carries the direction, negative on the side the money left"*, and — as this item amended it — *"**No field links the two entries to each other**"* with *"Since `ADR-0010` the two halves do carry **consecutive references**"* | the behaviour: `envel/summary.py:131` reads the direction off the sign and nothing else; observed as `4  2026-08-28  moved out  groceries  -20.00` and `5  2026-08-28  moved in  fun  20.00`, same `on`, same `at`, opposite `cents`, refs consecutive, and no pairing field on either. **This is the send-back's subject.** `envel/summary.py:123`–`:127`, the docstring above that line, no longer says *"nothing linking them"*; it now states the amended clause — no field names the pair, the halves take consecutive references since `ADR-0010`, no code reads that adjacency as a link. Checked as a claim, not only as a diff: `grep -rn "ref" envel/ \| grep -E "ref *[-+] *1"` → **exit 1, no output**, so nothing pairs them by adjacency |
| ADR-0008 | conforms | *"A month is the seven-character string `YYYY-MM`, and it is compared as a string"*, *"Every figure is a filtered sum over the entries naming the envelope"*, months parsed in `envel/dates.py` alone | `envel/summary.py:191` and `:196` compare months with `<` and `<=`, and `:215` with `>`; all three are string comparisons and there is no calendar arithmetic in the new code. `bounded_balance` at `:182` is the filtered sum, with the bound passed in — **nothing subtracts one figure from another**. **Enumeration, mine:** `grep -rn "parse_month" envel/ --include=*.py` → `envel/dates.py:67` (the definition) and `envel/cli.py:144` and `:151` (the two call sites). No parsing elsewhere |
| ADR-0009 | conforms | *"It returns `envelopes.Ok` or `envelopes.Refusal` … so `cli` dispatches it exactly as it dispatches the other five and gains no new branch shape"*, and reporting lives in its own module | `list_entries` at `envel/summary.py:199` returns `Refusal` at `:216`/`:221` and `Ok` at `:228`/`:229`/`:252`, and nothing else. `envel/cli.py:140` is one `elif` in the existing chain; the dispatch at `:165`–`:166` is untouched. **Enumeration, mine:** `ls envel/` → `cli, dates, envelopes, money, store, summary` — the listing is in `summary.py` beside `summarise`, and there is no third reporting module |
| ADR-0010 | conforms | *"An entry carries `ref`, a positive integer, written when the entry is appended and never changed afterwards"*, *"The counter is the only source of a new reference. Nothing derives one from a position, a length or a maximum"*, *"A document read at `format: 1` is **upgraded in memory**"* | `envel/envelopes.py:41` `take_ref` reads `store["next-ref"]` and advances it; no `max(`, no `len(` and no index in that path. Observed in a store the tool wrote: refs `1..9` with `next-ref: 10`, a move taking `4` then `5` with the outgoing side first, and every entry of every kind carrying one. **Upgrade in memory:** a format-1 store read by this branch produced a full listing and its md5 was **unchanged**; `main` read the same pristine copy and produced byte-identical output |

## Invalidation set

Twenty-nine entries, every one disposed. **This round reopened them again**, at this head. The
documents under `docs/` are byte-identical to the previously verified commit —
`git diff --stat 00b2b31..HEAD -- docs/` is **empty** — so what changed under them is the source,
and the source changed by one docstring hunk. Each row below says what I opened and what I ran. I
wrote no document.

| document | disposition | what I reopened, and what I found |
|----------|-------------|-----------------------------------|
| `docs/architecture/overview.md` `## The parts`: the `summary.py` row | verified-still-true | Reopened the row. It says *"the reports, both of them"*. `grep -n '^def ' envel/summary.py` → twelve functions, of which `summarise` and `list_entries` are the two reports and there is no third. True |
| `docs/architecture/overview.md` `## The parts`: dependency direction | verified-still-true | **Enumeration, mine:** every import in `envel/*.py` → `cli`: dates, envelopes, money, store, summary (**five**); `summary`: dates, envelopes, money; `envelopes`: copy, dates, money; `store`: json, os, pathlib; `money`: re; `dates`: datetime, re. **Falsifier:** an import of `summary` in `envelopes`, or of anything above in `store`/`money`/`dates`. None present. True |
| `docs/architecture/overview.md` `## The shape of it`: nothing below `cli` prints or exits | verified-still-true | **Enumeration, mine:** `grep -n "print(\|sys\.exit" envel/*.py` → four members, `envel/cli.py:158`, `:162`, `:168` and `envel/__main__.py:8` — all in `cli` or **above** it. **Falsifier:** a `print` in `store.upgraded` or in `summary.list_entries`; neither has one. True |
| `docs/architecture/overview.md` `## The shape of it`: write only if something changed | verified-still-true | **Enumeration, mine:** `grep -rn "store\.save" envel/*.py` → **one** call site, `envel/cli.py:166`, guarded by `if result.changed` at `:165`. **Boundary, the case that matters:** a `format: 1` store — the one the read upgrades in memory — was listed by this branch and its md5 was **unchanged**; the same file read by `main` gave byte-identical output. True |
| `docs/architecture/overview.md` `## The data`: one JSON document, derived balance | verified-still-true | Reopened against a store this branch wrote: one JSON document, an `envelopes` list, an `entries` list, and **no** stored balance field on any envelope. `envel list` recomputed 232.51 from the entries. True |
| `docs/architecture/overview.md` `## The data`: `at` on every kind, *"one field more"* | verified-still-true | Reopened against the same store. `at` is on all eleven entries of all three kinds. `move − income = ['on']`, exactly one. `spend − income = ['description', 'on']` — two, but `description` is optional and predates this item, and an **undescribed** spend differs by exactly `on`, which is the boundary. Recorded as observation 3 rather than a defect: this change did not move the differential, since `ref` went onto every kind. True as written |
| `docs/architecture/overview.md` `## The data`: the move-link sentence | to-update | Updated: `overview.md` is at **version 8** with a change-log row (eight rows for eight versions). The new text — *"No field in the file names the pair … the two consecutive references they take … No code reads that adjacency as a link"* — is what I checked for ADR-0007 above, against a store the tool wrote and a grep for `ref ± 1` that returns nothing. **This is the sentence the send-back was about**, one level down: the document was right and the source contradicted it, and now does not |
| `docs/architecture/overview.md` `## Conventions`: months parsed in `dates.py` alone | verified-still-true | **Enumeration, mine:** `grep -rn "parse_month" envel/ --include=*.py` → `envel/dates.py:67` and the two call sites `envel/cli.py:144`, `:151`. **Falsifier:** a month parsed inside `summary.py`; there is none. True |
| `docs/architecture/overview.md` `## Conventions`: two decimal places, no symbol | verified-still-true | **Enumeration, mine:** `grep -n "money.format_amount" envel/summary.py` → `:81` (the summary), `:148` (the entry line), `:235` and `:248` (AC9's brackets) — every amount this item prints. **Falsifier:** a conversion outside `envel/money.py`; `grep` for `100`, `Decimal` or `round(` outside it → exit 1. Observed: `-100.00`, `20.00`, `232.51`, `-67.49` |
| `docs/architecture/overview.md` `## Conventions`: stdout/0, stderr/non-zero | verified-still-true | Triggered, not read: four refusals (`nosuch`, `2027-03`, `2026-8`, `august`) each gave empty stdout and a non-zero exit, and four successes (`entries`, `entries groceries`, `entries --month 2026-08`, `entries car --month 2026-07`) each gave empty stderr and exit 0. True |
| `docs/architecture/overview.md` `## What is not decided yet` | verified-still-true | Reopened. The sentence predicts `ADR-0002` will be built on *"without changing the file's shape"*, and `ADR-0010` did change it. The row's disposition rests on the repair of the surrounding paragraph in version 8, which now records `ADR-0010` and removes `WI-0006` from the undecided list. Read against the document at this head: the sentence as it now stands is true |
| `docs/architecture/overview.md` `## Engagement state` | owned-by-ending | **Left alone, and checked that it was.** The section between `## Engagement state` and the next `## ` is **byte-identical** to `main`: md5 `6fd22866…` on both. No repair, no tidy |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` `## Decision`: worked document, `format` bullet | to-update | Updated: **version 3**, three change-log rows, and a `provenance` entry in `## Corrections`. The `format` bullet now cites `ADR-0010` as the branch it anticipated. Checked against `envel/store.py:11` (`FORMAT = 2`), `:17` (`READABLE = (1, 2)`) and `:83` (the check on load) |
| `docs/architecture/adr/ADR-0002-…` `## Corrections`: *"still reads and writes `FORMAT = 1`"* | verified-still-true | Reopened. The sentence is **false of today's code** (`FORMAT = 2`) and correctly left standing: `## Corrections` is append-only by `spec/doc-header.md` §4b and an entry is a **dated record** of what was observed then. `implement` found this mid-change and added the row rather than editing the entry. I agree with the disposition |
| `docs/architecture/adr/ADR-0002-…` `## Decision`: append-only, balance as a sum | verified-still-true | Reopened against the code: `envel/summary.py:164` builds a new list, `:170` returns `sorted(...)`, and the stored list is never reordered. `bounded_balance` at `:182` sums `cents` with no branch on `kind` — `grep "kind"` inside the three balance functions → no matches. **Boundary:** a format-1 store listed twice, md5 unchanged. True |
| `docs/architecture/adr/ADR-0002-…` `## Consequences`: *"neither needing a format change"* | verified-still-true | Reopened. The sentence is about `WI-0002` and `WI-0003` and is a prediction about **those two items**, both of which are `done` and neither of which changed the format. This item does, which is why it is in the set; the sentence's subject is unchanged. True as scoped |
| `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` | to-update | Updated: **version 2**, one change-log row, one `erratum`. `## Decision` now says the module holds the reports rather than the summary. Checked: `grep -n '^def ' envel/summary.py` shows `summarise` and `list_entries` in that one module, and `ls envel/` shows no third reporting module |
| `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md` `## Consequences`: *"Nothing computes the carried-in figure"* | to-update | Updated: **version 2**, one change-log row, one `erratum`. Checked at the code: `balance_before` (`:191`) and `balance_through` (`:196`) are both `bounded_balance` with a different bound — **a filtered sum, not a subtraction**. **Boundary, and it is load-bearing:** mutating `falls_in < month` to `<=` made 4 tests fail, so the bound is doing the work rather than decorating it |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` | to-update | Updated: **version 3**, two change-log rows, two `erratum` entries, each quoting the removed text verbatim. **This is the entry the send-back came from.** The document was already right after round 1; what was wrong was `envel/summary.py`'s docstring, which quoted the struck sentence back. At this head `grep -rn "nothing linking\|not linked\|linking them\|no link" envel/ tests/` → **exit 1, no output**, and `envel/summary.py:123`–`:127` states the amended clause instead |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` `## Decision`: `on` never absent | verified-still-true | **Enumeration, mine:** `grep -n '"kind": "spend"' envel/envelopes.py` → one site, `:168`; `:171` writes `"on"` unconditionally. **Falsifier:** a spend with no `on`, which would list under the day it was typed. **Boundary:** a spend recorded 2026-09-11 with `--on 2026-08-14` listed under 2026-08-14. True |
| `docs/architecture/adr/ADR-0003-store-location.md` | verified-still-true | **Enumeration, mine:** `grep -rn "ENVEL_FILE\|XDG_DATA_HOME\|\.local\|pathlib\|expanduser" envel/ --include=*.py` outside `envel/store.py` → **exit 1, no output**. The new code in that module, `upgraded`, takes a document rather than a path. True |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | verified-still-true | **Enumeration, mine:** `grep -rn "100\b\|Decimal\|round(" envel/ --include=*.py` outside `envel/money.py` → **exit 1, no output**. Every amount this item prints is one of the four `format_amount` calls listed above. True |
| `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` | verified-still-true | Run, not read: `python3 bin/envel entries groceries --month 2026-08` and `python3 -m envel entries groceries --month 2026-08` → stdout md5 `0be164c3…` on **both**. Neither entry point was edited by this branch. True |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` | verified-still-true | **Enumeration, mine:** every import across `envel/*.py` and `tests/*.py` → twelve standard-library names and the project's own modules; nothing third-party. Both commands run here: `python3 -m unittest discover -s tests -t .` exit 0 with 231 tests, `python3 -m compileall -q envel tests` exit 0. True |
| `docs/product/vision.md`: the reference is one number, and stays that entry's | verified-still-true | **Enumeration, mine, over a store this branch wrote:** refs `[1,2,3,4,5,6,7,8,9,10,11]`, all **distinct**, `next-ref` 12; `fun`'s first is **3** and `car`'s is **7**, so the count is across everything and not per envelope. **Falsifier:** a duplicate or a per-envelope restart. Second clause, boundary: after two more entries were recorded, the five references an earlier listing printed named the same entries character for character. True |
| `docs/product/vision.md`: the listing paragraph | verified-still-true | Reopened sentence by sentence against the four invocations at AC1: what it shows (AC2), the month it covers (AC7), the optional envelope (AC1, AC10), *"so that the lines add up to the balance"* (AC9: 0.00 − 34.99 − 12.50 − 20.00 = −67.49, printed). True |
| `docs/product/vision.md`: *"a listing of an envelope's entries"* | to-update | Updated: **version 7**, one change-log row. The text now reads *"off one envelope's entries, or off the month's across the envelopes"*. Checked against both forms run here — `envel entries groceries --month 2026-08` and `envel entries --month 2026-08` — and against `WI-0006/Q-003`, whose answer is that the envelope is optional |
| `docs/product/vision.md`: not connected to anything | verified-still-true | **Enumeration, mine:** the import list above — `argparse, copy, dataclasses, datetime, json, os, pathlib, re, subprocess, sys, tempfile, unittest`. **Falsifier:** `socket`, `urllib`, `http`, `requests` or any network name. None present, and this branch added none. True |
| `docs/product/vision.md` `## Engagement state` | owned-by-ending | **Left alone, and checked that it was.** Byte-identical to `main` between `## Engagement state` and the next `## `: md5 `4c18d819…` on both |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` at this head → exit 0, `Ran 231 tests in 26.6s … OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → `checked 7 item(s), 12 document(s); 0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | the `## Criteria` table: fifteen rows, each a command run here with its actual output. No row cites `impl-report.md` |
| `negative-cases-exercised` | **pass** | fifteen conditions triggered — see `## Negative and boundary cases exercised` |
| `a-criterion-about-criteria-is-read` | **pass** | AC14: `WI-0003`'s AC1–AC14 named and given a per-criterion verdict in `## AC14 — the read`, with the nine-invocation comparison as evidence for the reading. Non-intersection: **none to state**, because `test_one_store_listed_and_then_summarised_gives_both_answers` exercises both commands over one store |
| `adr-conformance-is-decided` | **pass** | `lint-documents --rule adr-conformance-is-decided --item WI-0006` → exit 0, *"10 binding ADR(s), 10 conformance row(s)"* |
| `invalidation-set-is-disposed` | **pass** | `lint-documents --rule invalidation-set-is-disposed --item WI-0006` → exit 0, *"29 invalidation entr(y/ies) against 29 row(s) in the verification report"* |
| `tests-would-fail-without-the-change` (advisory) | **pass, with one declared exception** | twelve mutations applied to the source at this head, eleven caught — see `## Test sensitivity check` |

## Negative and boundary cases exercised

Each of these was **triggered** here, not read about.

1. `envel entries nosuch` — unknown envelope. stdout empty, stderr `there is no envelope called 'nosuch'. Nothing has been listed.`, exit 1.
2. `envel entries --month 2027-03` — a month later than this one. stdout empty, exit 1, `2027-03 has not happened yet…`.
3. `envel entries --month 2026-8` — one-digit month. Refused, exit 1.
4. `envel entries --month august` — a word. Refused, exit 1.
5. `envel entries --month 2026-13` — month 13. Refused, exit 1.
6. `envel entries --month 2026-08-01` — a full date where a month goes. Refused, exit 1.
7. `envel entries car --month 2026-07` — an envelope with **no** entries in the month. Success, exit 0, brackets still printed, `nothing was recorded against car in 2026-07` between them.
8. `envel entries --month 2026-07` — a month with **nothing at all** in it, no envelope named. Success, exit 0, `nothing was recorded in 2026-07`, and **no** bracket lines.
9. `envel entries groceries extra` — a word too many. `usage: envel entries [-h] [--month YYYY-MM] [name]` on stderr, exit 2, stdout empty.
10. `envel entries --month` with nothing after it. `error: argument --month: expected one argument`, exit 2.
11. `envel entries --for 2026-08` — an option this subcommand does not have. `error: unrecognized arguments: --for`, exit 2.
12. `envel entries --month 2026-09` — the month today falls in, the boundary of case 2. **Not** refused: exit 0.
13. `envel entries GROCERIES --month 2026-08` — capitalisation, the boundary of case 1. Accepted, identical output to `groceries`.
14. Two entries sharing one date (`2026-08-14`, refs 8 and 9) — AC8's tie. Printed in storage order, twice, identically.
15. A **format-1** store read by this branch — the upgrade boundary. Listed in full, md5 of the file **unchanged**, and byte-identical output from `main` on a pristine copy.

## Test sensitivity check

Twelve mutations, applied to the source at this head, each followed by
`python3 -m unittest tests.test_entries tests.test_cli` (115 tests) and then restored. `git status
--short envel/` was empty afterwards.

| # | mutation | criteria it attacks | tests |
|---|----------|--------------------|-------|
| M1 | `take_ref` returns `len(entries) + 1` instead of the document's counter | AC3, AC4 | **OK — not caught.** Declared below and in `## Not verified, and why` |
| M1b | `take_ref` returns a constant instead of the counter | AC3 | FAILED (2) |
| M2 | `entries_in` sorts `reverse=True` | AC8 | FAILED (2) |
| M3 | `balance_before`'s bound widened from `< month` to `<= month` | AC9 | FAILED (4) |
| M4 | `entry_kind` reads the move direction off the wrong side of the sign | AC6 | FAILED (3) |
| M5 | the future-month refusal removed from `list_entries` | AC13 | FAILED (3) |
| M6 | the unknown-envelope refusal removed | AC12 | FAILED (1 + 1 error) |
| M7 | the nothing-to-show line replaced by an empty listing | AC11 | FAILED (6) |
| M8 | the opening and closing lines printed when no envelope is named | AC10 | FAILED (8 + 10 errors) |
| M9 | the description dropped from the line | AC2 | FAILED (1 + 1 error) |
| M10 | `entry_date` always takes `at`, never `on` | AC5 | FAILED (3) |
| M11 | a running-balance column appended to every listing line | AC14 | FAILED (4) |
| M12 | the default month is a fixed month instead of the month today falls in | AC1, AC7 | FAILED (2) |

**M1 is the one that did not fail, and it is the same one the previous round found.** Counting
`len(entries) + 1` is behaviourally identical to reading the counter **today**, because nothing in
the tool removes an entry, so the two can only diverge once `WI-0005` exists. M1b — a constant —
does fail, so the tests do hold the references to being distinct and counted across envelopes; what
they cannot yet hold is the difference between a stored number and a derived one. Declared in
`## Not verified, and why`, owned by `WI-0005`, which already records `depends-on: WI-0006`.

**The docstring this round changed is not mutation-testable**, and no test was written for it: it is
a comment. Its correctness was checked as a **claim** instead — each of its three sentences against
`ADR-0007` `## Decision`, `overview.md` `## The data`, and a store the tool wrote. That check is in
the ADR-0007 row of `## ADR conformance`.

## Defects found

**None.** The send-back's single finding is fixed and was checked directly:

```
$ grep -rn "nothing linking\|not linked\|linking them\|no link" envel/ tests/
$ echo $?
1
```

The replacement text was not accepted on sight. Each of its three claims was checked against what it
restates and against a store the tool wrote — the ADR-0007 row of `## ADR conformance` has the three
of them with their evidence.

No bug item was filed. Nothing in the diff belongs to another item.

## Observations

Not defects — no criterion says otherwise — but a reader of this record should have them. All three
were recorded by the previous round and all three were **re-confirmed here**.

1. **A store this branch writes cannot be read by the previous version.** Reproduced deliberately
   this round: `main`'s binary given a format-2 store printed
   `/tmp/wi6v2/s.json is not an envel store of format 1. Nothing has been changed.` on all nine
   invocations and wrote nothing. This is `ADR-0010`'s declared consequence — *"Reversibility: hard,
   and it gets harder with use"* — and the refusal is `ADR-0002` behaving as designed. It is worth
   the stakeholder knowing the upgrade is one-way in practice.
2. **`envel entries` spells a month `--month`; `envel summary` spells it as a plain word.** Confirmed
   here: `envel summary --month 2026-08` → `usage: envel summary [-h] [YYYY-MM]`, exit 2, so
   `WI-0003` AC1 still holds. Not a criterion failure and not an unrecorded decision — `refine` spent
   the `WI-0003/Q-004` delegation on it deliberately and priced a disagreement at an amendment to AC1
   and AC15. It is the thing most likely to surprise the stakeholder at sign-off.
3. **`overview.md`'s *"A spend and a move each carry one field more"*** is literally two on a
   described spend, because `description` is optional. Checked at the boundary this round: an
   **undescribed** spend differs from income by exactly `on`. It predates this item, which put `ref`
   on every kind and so did not move the differential. Recorded rather than sent back.

## Not verified, and why

1. **That a reference survives a *removal*.** AC4's promise — *"a number I wrote down last week
   still means what it meant"* — is fully observable only once something removes an entry, and
   nothing in this item does. What was verified is the half that is observable: recording more
   entries moves nobody's reference. M1 above proves the limit rather than asserting it: deriving
   the number from `len(entries) + 1` passes every test today. The item that makes it observable is
   `WI-0005`, which adds `envel remove` and records `depends-on: WI-0006`.
2. **A month boundary across a year end.** No criterion names one. Month comparison is string
   comparison over zero-padded ISO, so `2026-12 < 2027-01` holds by construction; there is no code
   for it to be wrong in.
3. **Two invocations writing at once.** Concurrency is in no item's scope. `ADR-0002`'s atomic write
   is the whole of what exists, and this item added nothing to it — it added a **read** that does not
   write, which is case 15 above.
4. **Anything about `envel fix` or `envel remove`.** They do not exist on this branch; they are
   `WI-0005`.
5. **The docstring by test.** There is no test for a comment and none was added. It was checked as a
   claim instead, three sentences against three sources — see `## Defects found` and the ADR-0007
   row.
