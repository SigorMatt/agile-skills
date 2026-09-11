# Verification report — WI-0003

Verified-commit: 6eb35e318f640e0c35d550c03ac07cc06c87e7f3

## Verdict

**Pass.** All fourteen acceptance criteria are met, each decided by a command this execution ran
against the branch head with `ENVEL_FILE` pointed at a scratch store. No defect was found, no bug
item was filed, and no document was written.

The strongest evidence is not any single criterion. The four figures were **recomputed
independently** — a script that reads the store's JSON and rebuilds *in*, *spent*, *moved* and
*left* from the criteria's own words, without importing `envel.summary` — and compared against
what the tool printed for every envelope in every month of two stores. Every row matched, and the
reconciliation identity of AC3 was asserted inside that script for each envelope and month rather
than read off the code
`[src: run: python3 - (an independent recomputation over /tmp/vfy/a.json and /tmp/vfy/c.json) → exit 0, 4 month(s) across 2 store(s), every one MATCH]`.

Two things are worth a reader's attention and neither is a defect in the item. The first is that
my own mutation harness produced a false negative and then left the workspace looking broken;
both are recorded under `## Test sensitivity check`, because the first is the trap `WI-0004`'s
verification already hit once and the second is a new face of it. The second is the F-084 forced
gate on `implement`'s closing transition, which I re-ran and confirmed: `validate-workspace`
reports 0 errors on the branch head.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | `bin/envel summary 2026-08` and `bin/envel summary --month 2026-08`, against a seeded store | `fun  in 0.00  spent 0.00  moved -30.00  left 0.00` / `groceries  in 0.00  spent 20.00  moved 30.00  left 60.00`, exit 0; and `usage: envel summary [-h] [YYYY-MM]` / `envel summary: error: unrecognized arguments: --month` on stderr, exit 2, stdout empty | Both halves of the criterion: the month is a plain word, and `--month` is refused as a wrong command line per AC14. The third clause — *"`summary` takes no argument other than the month"* — is `bin/envel summary 2026-08 extra` → exit 2, same usage line |
| AC2 | pass | `bin/envel summary` over a store built entirely through `new`/`add`/`spend`/`move` | `apples  in 1200.00  spent 18.50  moved -20.00  left 1161.50` / `Fun  in 50.00  spent 0.00  moved 20.00  left 70.00` / `zebra  in 0.00  spent 0.00  moved 0.00  left 0.00` | One row per envelope, four figures each. The move is in the third figure and **not** the second: `apples` spent 18.50, which is 12.50+3+3, the three spends only, while its 20.00 move shows as `moved -20.00`. The criterion's own net example was run separately: an envelope that received 50.00 and gave away 20.00 → `taker  in 30.00  spent 0.00  moved 30.00  left 60.00`, i.e. **30.00**, the number the criterion names |
| AC3 | pass | `bin/envel summary 2026-08` over a store with 50.00 carried in from July, 20.00 spent and 30.00 moved in during August; then an independent recomputation over every envelope and month of two stores | `groceries  in 0.00  spent 20.00  moved 30.00  left 60.00` — the criterion's worked example verbatim, and 50.00 + 0.00 − 20.00 + 30.00 = 60.00. The recomputation reported `2026-07 MATCH`, `2026-08 MATCH`, `2026-09 MATCH`, `2026-09 MATCH` | The identity `left == carried_in + in − spent + moved` was asserted for **12** (envelope, month) pairs inside the recomputation script, which computes `carried_in` itself from the months before the one summarised. The tool never computes a carried-in figure, so the two arithmetics are genuinely independent |
| AC4 | pass | `bin/envel summary 2026-06` against a store whose earliest envelope was created in July; `bin/envel summary 2026-04` against a store created in May | `no envelopes existed in 2026-06`, exit 0, stderr empty; `no envelopes existed in 2026-04`, exit 0 | A success, not a refusal. The criterion's own exclusion was checked at the boundary: `bin/envel summary 2026-06` against a store whose envelope existed since May but had no activity in June prints `savings  in 0.00  spent 0.00  moved 0.00  left 123.45` — a row of zeros, **not** the nothing-to-print line. A store path that does not exist at all is the same empty case and still exits 0 |
| AC5 | pass | `bin/envel summary` compared with `bin/envel summary 2026-09`, with `date -u` read on the same run; then `bin/envel summary 2026-07` | `date -u +%Y-%m-%d` → `2026-09-11`; the two outputs are byte-identical (`diff` empty); `summary 2026-07` → `fun  in 30.00  spent 0.00  moved 0.00  left 30.00` / `groceries  in 50.00  spent 0.00  moved 0.00  left 50.00` | Bare is the month today falls in; a named month is that month; a month that has ended is still reachable after it has ended. The `YYYY-MM` form is AC12's subject and is decided there |
| AC6 | pass | `bin/envel summary` over a store with three **described** spends and three envelopes, piped through `grep -n 'tea\|bread\|milk\|total\|Total\|TOTAL'` and `wc -l` | grep exit 1 — no match; `wc -l` → 3, and `bin/envel list \| wc -l` → 3 | No total line, no individual spends, and exactly one line per envelope — the summary's line count equals the delivered listing's. The three descriptions are in the store and appear nowhere in the output |
| AC7 | pass | `bin/envel summary 2026-08` before and after `bin/envel new car` + `bin/envel add car 25`, compared with `diff`; then `bin/envel summary 2026-09` | `diff` reported no difference — `IDENTICAL`; and September shows `car  in 25.00 …` / `fun  in 0.00  spent 0.00  moved 0.00  left 0.00` / `groceries  in 0.00  spent 0.00  moved 0.00  left 60.00` | All three clauses: an envelope created after the month gets no row; a past month reads the same however long afterwards; an envelope with no activity gets a row of three zeros and its **carried-over** balance (`groceries`, 60.00 in a month in which nothing happened to it) |
| AC8 | pass | a store in which one income and one spend were **both** recorded on 2026-09-02, the spend held against 2026-08-29; `bin/envel summary 2026-08` and `bin/envel summary 2026-09` | August: `payslip  in 0.00  spent 42.30  moved 0.00  left -42.30`. September: `payslip  in 2000.00  spent 0.00  moved 0.00  left 1957.70` | This is the asymmetry itself, isolated: two entries typed at the same moment, the income counted in the month it was **typed** and the spend in the month it **happened**. `envel add` is unchanged — `git diff main...HEAD --stat -- envel/envelopes.py` is empty |
| AC9 | pass | `bin/envel summary 2026-10`, `bin/envel summary 2027-03`, `bin/envel summary 2026-09` — each with stdout, stderr and the exit code captured separately | `2026-10 has not happened yet, so there is nothing to summarise. The month this one is in is 2026-09.` on **stderr**, stdout empty, exit 1; the same for 2027-03; and 2026-09 → exit 0, three rows on stdout, stderr empty | The boundary is the criterion's whole point and was exercised on both sides: **next** month refused, **this** month not refused, on 2026-09-11 when most of September has not happened |
| AC10 | pass | `bin/envel summary \| cut -d' ' -f1` compared with `bin/envel list \| cut -d' ' -f1` over envelopes named `zebra`, `Fun`, `apples` | both `apples` / `Fun` / `zebra`; `diff` reported no difference | Alphabetical ignoring capitalisation, and demonstrably **the same order the delivered listing prints**, which is what the criterion cites. `Fun` between `apples` and `zebra` is the case a case-sensitive sort would get wrong |
| AC11 | pass | every row of every summary across five stores, parsed and each amount token matched against `^-?\d+\.\d\d$` and scanned for `£ $ € ,` | **60** amount tokens checked, `violations: none` | Includes a zero (`0.00`), a negative (`-30.00`), an amount over a thousand written with no separator (`1200.00`) and one over ten thousand (`2000.00`), so the separator clause had a case that could have failed |
| AC12 | pass | `bin/envel summary <m>` for each of `2026-8`, `08-2026`, `august`, `2026-13`, `2026-08-01`, and `2026-00` | each → exit 1, stdout **empty**, stderr `'<m>' is not a month: write it as YYYY-MM, such as 2026-08` | Every form the criterion names, plus the other end of the range. *"No row is computed"* was checked through a case that distinguishes the two refusals: `bin/envel summary 2027-13` is both unreadable and in the future, and the message returned is the **month-form** one, so the month check fired before `summarise` — the only place a row could be computed — was reached |
| AC13 | pass | one invocation per criterion it names, ten in all, each with stdout, stderr and the exit code read off the same run | AC9 exit 1 / stdout empty / stderr 1 line; AC12 exit 1 / empty / 1 line; AC14 exit 2 / empty / 2 lines; AC1, AC2, AC4, AC5, AC6, AC7, AC8 each exit 0 / non-empty stdout / **empty** stderr. `all ten as the convention requires: True` | A criterion whose subject is other criteria — read per criterion in `## A criterion about criteria` below, not settled by the suite being green |
| AC14 | pass | `bin/envel summary --month 2026-08`, `bin/envel summary 2026-08 extra`, `bin/envel summary a b c` | each → exit 2, stdout empty, stderr beginning `usage: envel summary [-h] [YYYY-MM]` then `envel summary: error: unrecognized arguments: …` | The usage message is the **subcommand's**, which is what the criterion asks for. `bin/envel` with no subcommand prints `usage: envel [-h] {new,add,list,spend,move,summary} ...`, so `WI-0001` AC14 — the usage naming the subcommands the tool has — is not falsified by the new one |

## A criterion about criteria

AC13's subject is other criteria. It names them, so it is decidable: refusals at **AC9, AC12,
AC14**; successes at **AC1, AC2, AC4, AC5, AC6, AC7, AC8**. Per criterion, read against the
delivered behaviour:

| criterion it covers | its own sentence about streams | still true of the new behaviour? |
|---|---|---|
| AC9 | *"nothing is printed, a message … goes to stderr, and the command exits non-zero"* | **yes** — exit 1, stdout empty, one line on stderr |
| AC12 | *"refused with a message, nothing is printed on stdout"* | **yes** — exit 1, stdout empty, the message on stderr. AC12 does not itself name a stream; AC13 supplies it and the run satisfies both |
| AC14 | *"a usage message for the subcommand on stderr and a non-zero exit, and nothing … on stdout"* | **yes** — exit **2**, not 1. AC13 says *"non-zero"* and AC14 says *"non-zero"*, so 2 satisfies both; the two sentences do not collide, and this is the one place they could have |
| AC1 | the summary is printed | **yes** — exit 0, rows on stdout, stderr empty |
| AC2 | one row per envelope with four figures | **yes** — same run as AC1 |
| AC4 | *"prints to stdout a line saying so, and exits 0"* | **yes** — AC4 names its own stream and exit code, and they agree with AC13's |
| AC5 | the month today falls in, or a named one | **yes** — exit 0, stderr empty |
| AC6 | no total line, no individual spends | **yes** — a success; exit 0, stderr empty |
| AC7 | a row for every envelope that existed | **yes** — exit 0, stderr empty |
| AC8 | the money-in figure | **yes** — exit 0, stderr empty |

**Non-intersection: there is none to declare, and that was checked rather than assumed.** The one
place two of these sentences could contradict each other is the exit code — AC14 is satisfied by
argparse's 2 while AC13 says only *"non-zero"* — and both sentences were quoted above and read
against the same run rather than against each other's summary. Every one of the ten criteria has
an executable case that exercises it **together with** AC13's claim, because the check is one
invocation per criterion with all three streams read off it; nothing here rests on the suite being
green. Nothing is waived.

## ADR conformance

| ADR | verdict | clause quoted from its Decision | file and line, or why not engaged |
|-----|---------|--------------------------------|-----------------------------------|
| `ADR-0001` | conforms | *"Two functions in `envel/money.py` are the only places the two forms meet … No other module converts between them, and no amount is ever held as a `float`"* | `envel/summary.py:68` is the module's only contact with the text form, `money.format_amount(cents)`; the four figures are `int` throughout `envel/summary.py:52-56`. Enumerated: `grep -rn 'int(whole)\|% 100\|// 100\|\* 100\|float(' envel/*.py` → 2 lines, `envel/money.py:34` and `envel/money.py:42`, and nothing in `summary.py` |
| `ADR-0002` | conforms | *"`entries` is append-only within a run and ordered as written. An envelope's balance is the sum of `cents` over the entries naming it"* | `envel/summary.py:55` — `left = sum(entry["cents"] for entry in mine if entry_month(entry) <= month)`, the ADR's own sum with a month bound and no branch on kind. Nothing is appended, sorted or written: `md5sum` of the store is unchanged across three summary runs including a refusal. `format` stays `1` |
| `ADR-0003` | conforms | *"The store path is, in order: 1. `$ENVEL_FILE`, used exactly as given"* … *"One function in `envel/store.py` resolves the path and nothing else knows about it"* | `envel/cli.py:98` is the only caller; `grep -n 'ENVEL_FILE\|XDG\|store_path\|pathlib\|open(' envel/summary.py` → exit 1, no output. Every criterion above was observed against a scratch `ENVEL_FILE`, and a path that does not exist is the empty store — `ENVEL_FILE=/tmp/vfy/deep/dir/store.json bin/envel summary` → exit 0 |
| `ADR-0004` | conforms | *"there are two ways to start it, both reaching the same `main`"* | `envel/__main__.py:5` (`from envel.cli import main`) and `bin/envel:9` are the two entry points, and the subcommand they now both reach is added at `envel/cli.py:73` and dispatched at `envel/cli.py:123`. Observed: `ENVEL_FILE=… python3 -m envel summary 2026-08` and `ENVEL_FILE=… bin/envel summary 2026-08` printed byte-identical output; `python3 -m envel summary --month 2026-08` → exit 2 with the same usage line. The new subcommand is reachable from both, which is the shape that would have falsified it |
| `ADR-0005` | conforms | *"`commands.test`: `python3 -m unittest discover -s tests -t .`"*, *"`commands.lint`: `python3 -m compileall -q envel tests`"*, *"every file under `envel/` and `tests/` compiles"* | Both commands cover the two new files: `unittest discover -v \| grep -c test_summary` → **27**, and `compileall` produces `envel/__pycache__/summary.cpython-312.pyc` and `tests/__pycache__/test_summary.cpython-312.pyc`. No third-party import: `envel/summary.py:24` is `from . import dates, envelopes, money` and `tests/test_summary.py` imports only `copy`, `datetime`, `unittest` and the local package |
| `ADR-0006` | conforms | *"`on` is present on every spend entry, including one recorded without `--on` … It is never absent and never null, so a reader never has to fall back to `at`"* | `envel/summary.py:34` depends on exactly that, and the guarantee holds at its boundary: a spend recorded with **no** `--on` stores `on='2026-09-11'` (`envel/envelopes.py:152` writes it unconditionally), while the income beside it has `on=None`. Its `## Consequences` prediction — *"`WI-0003` sums a month's spending by `on`, a month's moves by `on`, and a month's income by `at`, with no branch on what a date means"* — is `envel/summary.py:34`, one expression with no `kind` in it |
| `ADR-0007` | conforms | *"`WI-0003`'s net figure for an envelope in a month is then the plain sum of `cents` over that envelope's `move` entries in that month — positive when more arrived than left"* | `envel/summary.py:54` — `moved = sum(entry["cents"] for entry in in_month if entry["kind"] == "move")`, a plain sum with no sign handling and no pairing of the two halves. Observed: `taker` received 50.00 and gave 20.00 → `moved 30.00`; `giver` gave 50.00 and received 20.00 → `moved -30.00` |
| `ADR-0008` | conforms | point 1: *"The month an entry falls in is `entry["on"][:7]` when the entry has an `on`, and `entry["at"][:7]` otherwise. One function, no branch on `kind`"*; point 3's filter table; point 4: *"Nothing is precomputed and nothing new is stored"*; point 5: *"An entry naming an envelope that is not in `envelopes` contributes to no row"* | Point 1 — `envel/summary.py:34`, via `envel/dates.py:87` (`text[:MONTH_LENGTH]`, `MONTH_LENGTH = 7` at `envel/dates.py:30`). Point 2 — `envel/summary.py:51`, `:55`, `:83`, `:91` are the only comparisons and all four are string `==`, `<=` or `>`; the module imports no `datetime`. Point 3 — `envel/summary.py:52-55` match the table row for row, `spent` negated at `:53`. Point 4 — `format` unchanged, store bytes unchanged. Point 5 — observed: a store carrying an income entry naming `gone`, which is in no `envelopes` list, prints one row for `groceries` with no `99.00` anywhere |
| `ADR-0009` | conforms | *"`envel/summary.py` holds the summary … It returns `envelopes.Ok` or `envelopes.Refusal` … `summary` imports `envelopes`; `envelopes` does not import `summary`"*, and *"`summary` prints nothing and calls no `sys.exit`"* | `envel/summary.py:84` and `:94`/`:95` return the two types; `envel/summary.py:24` imports `envelopes`, `money`, `dates`; `grep -n '^from\|^import' envel/envelopes.py` → `copy`, `dataclasses`, `datetime`, `from . import dates, money` — no `summary`. `grep -n 'print(\|sys\.exit'` over all five modules below `cli` → exit 1, no output, while the same grep over `envel/cli.py` finds 3, so it could have produced a counterexample |

**No ADR outside the plan's list was found engaged.** The nine cover the amounts, the store's shape
and location, the entry points, the checks, the two date fields, the move pair, and this item's own
two; `find docs/architecture/adr -name '*.md'` → 9 files, so the list is also complete by
exhaustion.

## Invalidation set

Twenty-seven entries. Every one carries a disposition: **24** `verified-still-true`, **2**
`owned-by-ending`, **1** `to-update`. None was left open.

| document | disposition | what I reopened, and what I found |
|----------|-------------|-----------------------------------|
| `docs/architecture/overview.md` `## The parts`, the `envel/summary.py` row | verified-still-true | Reopened. The row says the module owns *"the reports: a month's four figures per envelope, and the rows they print"*. `grep -n '^def ' envel/summary.py` → `entry_month`, `figures`, `row`, `summarise` — four functions, exactly a month's figures and the rows. True |
| `docs/architecture/overview.md` `## The parts`, *"`cli` knows about all five modules below it… `envelopes` does not know about `summary`"* | verified-still-true | Reopened as a quantified claim. Set: what `cli` imports — `sed -n '13p' envel/cli.py` → `from . import dates, envelopes, money, store, summary`, **five** members, each a module below `cli`; `ls envel/*.py` shows no sixth candidate (`__init__.py` is empty, `__main__.py` is above `cli`). Falsifier: an import of `summary` in `envelopes` — `grep -n import envel/envelopes.py` → `copy`, `dataclasses`, `datetime`, `from . import dates, money`; absent. True |
| `docs/architecture/overview.md` `## The shape of it`, *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | verified-still-true | Reopened. Set enumerated from `ls envel/*.py`: `dates`, `envelopes`, `money`, `store`, `summary`. Verdict per member: `grep -n 'print(\|sys\.exit'` over all five → exit 1, no output. The check could have failed: the same grep over `envel/cli.py` returns 3 hits. Checked **at** the new module, which is the one this change put at risk. True |
| `docs/architecture/overview.md` `## The shape of it`, *"write the whole store back, atomically, but only if something changed"* | verified-still-true | Reopened at the boundary this change creates — the first command that changes nothing. `md5sum` of the store before and after `summary 2026-08`, bare `summary`, and a refused `summary 2026-10`: `3e842f09493ede8eaa4f556709b18535` both times. True |
| `docs/architecture/overview.md` `## The data`, `at` on every kind, `on` on a spend and a move, income carrying none | verified-still-true | Reopened. Set: the kinds, enumerated from a store built by the delivered commands → `income`, `spend`, `move`. Verdict per member: income has no `on`; a spend recorded **without** `--on` still has `on='2026-09-11'`; a move has `on`. This change writes neither field — `git diff main...HEAD --stat -- envel/envelopes.py envel/store.py` is empty. True |
| `docs/architecture/overview.md` `## Conventions`, *"A date typed at the command line is written `YYYY-MM-DD`, and a month `YYYY-MM`, and nothing else"* | verified-still-true | Reopened as two falsifiers. Another spelling accepted: six forms tried at the command line, every one refused, including `2026-08-01` — a perfectly good **date** offered as a month, which is the boundary between the sentence's two halves. A month parsed outside `envel/dates.py`: `grep -rn 'parse_month\|_MONTH\|MONTH_LENGTH' envel/*.py` → six in `dates.py` and one call site in `cli.py`; no parser elsewhere. True |
| `docs/architecture/overview.md` `## Conventions`, *"Amounts are printed with exactly two decimal places and no currency symbol"* | verified-still-true | Reopened over output rather than code: 60 amount tokens across five stores, every one matching `^-?\d+\.\d\d$`, none carrying `£ $ € ,`. Falsifier available: a figure rendered by anything but `money.format_amount` would have shown as raw cents, and `grep -c format_amount envel/summary.py` → 1, at `envel/summary.py:68`, covering all four figures. True |
| `docs/architecture/overview.md` `## Conventions`, success to stdout with exit 0, refusals to stderr with a non-zero exit | verified-still-true | Reopened as the AC13 matrix above: ten invocations, five distinct new paths (a row, the nothing-to-print line, and three refusals), all three streams read off each run. True |
| `docs/architecture/overview.md` `## What is not decided yet`, naming two items | verified-still-true | Reopened. `WI-0003`'s design is in `ADR-0008` and `ADR-0009`, both of which exist and both of which this change implements (see `## ADR conformance`). The named falsifier is a `format` change: `grep -n FORMAT envel/store.py` → 4 lines, and `git diff main...HEAD --stat -- envel/store.py` is empty. True |
| `docs/architecture/overview.md` `## Engagement state` | owned-by-ending | Left exactly as it is, and confirmed untouched: `git diff main...HEAD -- docs/` has three hunks in `vision.md` only — the front matter, `## What it is for`, and the change-log table — and none in either document's `## Engagement state` |
| `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md` `## Decision`, points 1 to 5 and the filter table | verified-still-true | Reopened clause by clause; the full read is the `ADR-0008` row of `## ADR conformance`. True |
| `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md` `## Consequences`, *"Nothing computes the carried-in figure and nothing checks the identity"* | verified-still-true | Reopened over the module's 101 lines. The four sums at `envel/summary.py:52-55` are the only arithmetic; none is bounded by *months before* the month asked for, and no line compares the four figures with each other. Falsifier: my own recomputation script **does** compute a carried-in figure and assert the identity — that is what an independent check looks like, and it lives outside the module, which is what the sentence claims. True |
| `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` `## Decision`, the module's contents and the dependency edge | verified-still-true | Reopened; the full read is the `ADR-0009` row of `## ADR conformance`. True |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` `## Decision`, `WI-0003`'s net move figure | verified-still-true | Reopened. It was a prediction and is now a description: `envel/summary.py:54` is the plain sum, and the two directions were observed (`moved 30.00` and `moved -30.00` for the two sides of the same pair). True |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` `## Consequences`, *"sums … with no branch on what a date means"* | verified-still-true | Reopened. `grep -n kind envel/summary.py` → 7 lines: three in `figures()` selecting a **column** by kind, which is what AC2 asks for, and four in prose. `entry_month`'s body contains none, which is what the clause is about. True |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` `## Decision`, *"`on` is present on every spend entry … never absent and never null"* | verified-still-true | Reopened at the boundary — the case the sentence itself calls out, a spend recorded without `--on`. Observed: `on='2026-09-11'`. `grep -rn '"kind": "spend"' envel/*.py` → one writer, `envel/envelopes.py`, and `envel/envelopes.py:152` writes `on` unconditionally. True |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` `## Decision`, *"An envelope's balance is the sum of `cents` over the entries naming it"* | verified-still-true | Reopened. Falsifier: a kind special-cased to make `left` come out right. `envel/summary.py:55` mentions no kind, and the independent recomputation — which sums all three kinds alike — matched the tool for every envelope and month. True |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` `## Decision`, *"`entries` is append-only within a run and ordered as written"* | verified-still-true | Reopened. `grep -n 'sorted\|append\|\.sort(\|store\[' envel/summary.py` → 3 lines: one `sorted` over **envelopes** at `:99`, and two reads. The store's md5 is unchanged across three runs. True |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` `## Decision`, *"Two functions in `envel/money.py` are the only places the two forms meet"* | verified-still-true | Reopened. Set: every conversion in the package — `grep -rn 'int(whole)\|% 100\|// 100\|\* 100\|float(' envel/*.py` → exactly 2, both in `money.py`. True |
| `docs/architecture/adr/ADR-0003-store-location.md` `## Decision` and `## Consequences`, the resolution order and the one function | verified-still-true | Reopened. Falsifier: a store path inside `envel/summary.py` — `grep -n 'ENVEL_FILE\|XDG\|store_path\|pathlib\|open(' envel/summary.py` → exit 1, no output. True |
| `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` `## Decision`, two entry points *"both reaching the same `main`"* | verified-still-true | Reopened by running both against the same store: byte-identical output, and the refusal path through both too. True |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` `## Decision`, the two commands and what lint checks | verified-still-true | Reopened: 27 discovered tests in the new file, `.pyc` produced for both new files, no third-party import. True |
| `docs/product/vision.md` `## What it is for`, *"the summary's third column is a balance"* | to-update | The document **was** updated: `git diff main...HEAD -- docs/product/vision.md` shows `version: 2` → `3`, the sentence rewritten to name the last column and the fourth of four, and a new change-log row `\| 3 \| 2026-09-11T06:38:45Z \| implement \| WI-0003 \| …`. I checked that the repaired sentence is true rather than merely different: the column order printed is in, spent, moved, left, so the balance is the fourth; and it is still a balance and not a monthly remainder, which is `summary 2026-08` → `left 60.00` for an envelope that added nothing that month |
| `docs/product/vision.md` `## What it is for`, item 4, *"Looking at a summary of a month"* | verified-still-true | Reopened now that there is something behind it. `bin/envel summary 2026-08` looks at a summary of one month; the sentence says no more than that and nothing in it is false. True |
| `docs/product/vision.md` `## What it deliberately is not`, *"no server, no sync, no bank import, no network"* | verified-still-true | Reopened as a quantified claim over the whole package rather than over the new imports: `grep -rn 'socket\|urllib\|http\|requests\|ssl' envel/ bin/envel` → exit 1, no output. `envel/summary.py:24` imports only local modules. True |
| `docs/product/vision.md` `## What it deliberately is not`, *"no forecasts, no goals, no recommendations"* and *"no graphical, web or full-screen terminal interface"* | verified-still-true | Reopened at the boundary each would fail at. Forecasts: the tool's first report **refuses** a future month rather than projecting one — `summary 2026-10` → exit 1 — so the one place a projection could have appeared does not. Interface: `summary 2026-08 \| od -c \| grep -c '033'` → 0, no escape sequence; `grep -rn 'curses\|colorama' envel/` → exit 1. True |
| `docs/product/vision.md` `## Engagement state` | owned-by-ending | Left exactly as it is; confirmed untouched by the hunk inspection recorded two rows above. The document's version was bumped two sections away and this section was not edited |

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → exit 0, **176 tests**, run by this execution on `6eb35e3` |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | pass | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings. This is also the re-run that settles `implement`'s forced gate: the F-084 error it reported was the absence of its own closing journal entry, and with that entry present the workspace validates |
| `every-criterion-independently-checked` | pass | the fourteen rows of `## Criteria`, each carrying a command this execution ran and its actual output. `impl-report.md` is cited nowhere as evidence |
| `negative-cases-exercised` | pass | `## Negative and boundary cases exercised` below — fifteen conditions triggered, not read about |
| `a-criterion-about-criteria-is-read` | pass | `## A criterion about criteria` — AC13 read per criterion against ten named IDs, with the one possible collision (AC14's exit 2 against AC13's *"non-zero"*) quoted from both and resolved, and non-intersection checked and absent |
| `adr-conformance-is-decided` | pass | `python3 .claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item WI-0003` → exit 0; the read behind it is `## ADR conformance`, nine rows, each quoting a clause of that ADR's `## Decision` |
| `invalidation-set-is-disposed` | pass | `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0003` → exit 0; the read behind it is `## Invalidation set`, 27 rows |
| `tests-would-fail-without-the-change` | pass | advisory. `## Test sensitivity check` — fourteen boundary mutations of my own design, one per criterion, all fourteen make their named test fail |

## Negative and boundary cases exercised

Every one was triggered and its output read, not inferred:

1. `summary 2026-10` — next month, the near side of AC9's boundary → exit 1, stderr, empty stdout.
2. `summary 2027-03` — far future → exit 1.
3. `summary 2026-09` — **this** month, the far side of the same boundary, on 2026-09-11 → exit 0.
4. `summary 2026-8` → refused. 5. `summary 08-2026` → refused. 6. `summary august` → refused.
7. `summary 2026-13` — above the month range → refused. 8. `summary 2026-00` — below it → refused.
9. `summary 2026-08-01` — a valid **date** offered as a month → refused.
10. `summary 2027-13` — unreadable **and** in the future, to see which check fires first → the
    month-form message, so no row was computed.
11. `summary --month 2026-08` — an option where the subcommand takes none → exit 2, subcommand usage.
12. `summary 2026-08 extra` and `summary a b c` — words beyond the month → exit 2.
13. `summary 2026-06` against a store created in July — the empty case → one line, exit 0.
14. `summary 2026-06` against a store created in May with no June activity — the case AC4
    explicitly says is **not** the empty one → a row of zeros with the carried balance.
15. `ENVEL_FILE` pointing at a path that does not exist → the empty store, exit 0, not an error.

## Test sensitivity check

Fourteen mutations, one per criterion, designed here rather than taken from the implementation
report and deliberately **boundary-flavoured** rather than removals — `<=` to `<`, `>` to `>=`,
`nargs="?"` to `nargs="*"`, the folded sort key to the raw one, the two date fields swapped. Each
patch was checked to match exactly once in its named file before being applied, and the file was
restored afterwards. All fourteen make their named test fail
`[src: run: python3 /tmp/vfy/mutate-verify2.py → exit 0, 14 rows, every one "the named test FAILS"]`.

**The first run of that harness was wrong twice, and both are worth recording.**

1. **A false negative.** AC11's mutant — `money.format_amount(cents)` replaced by `str(cents)` —
   was reported as leaving its test passing. Run on its own, the same mutation fails the same test
   with `AssertionError: 'in 1200.00' not found in 'groceries  in 120000  spent 0  moved 0  left 120000'`.
   The cause is CPython's bytecode cache: it invalidates on the source's **mtime in whole seconds
   and its size**, the AC10 mutant and the AC11 mutant are *both* 4864 bytes against an original of
   4880, and the harness wrote them within the same second — so the subprocesses that run
   `bin/envel` executed AC10's compiled bytecode against AC11's source. This is `WI-0004`'s finding
   3 in a new form: there the harness patched the wrong function, here it ran the wrong bytecode.
2. **It left the workspace looking broken.** After the harness finished, the suite reported 17
   failures and 2 errors with a **clean `git diff`** — because the last mutation, `nargs="?"` to
   `nargs="*"`, is a same-length replacement, so the restored original again collided with the
   mutant's cached `.pyc`. Purging `__pycache__` restored 176 green with no source change. A
   verifier who had stopped at the failing suite would have sent a sound item back.

   The fix both times is the same and costs nothing: purge `__pycache__` between mutations and run
   the child processes with `PYTHONDONTWRITEBYTECODE=1`. The re-run above does both.

## Defects found

**None.** No criterion of this item failed, so there is nothing to send back, and no behaviour
delivered by another item was found wrong, so no bug item was filed.

Two observations that are **not** defects, recorded so nobody re-derives them as ones:

- **The month-boundary race the plan named is still open**, deliberately: `cli` defaults to
  `dates.this_month()` and `summarise` compares against `dates.this_month()`, so a run at exactly
  midnight on the first of a month could refuse the month it had just defaulted to. No criterion
  of this item reaches it; the plan named it and `implement` declared why closing it was not free
  (it would change a signature `ADR-0009` states). Worth a sentence to `review-close`, not a bug.
- **Income entered later than the month it arrived in stays in the month it was typed**, with no
  way to correct it. That is AC8 working exactly as specified, and the stakeholder accepted the
  cost knowingly at `WI-0003/Q-003`. `item.md` already records it as a knowing limitation.

## Not verified, and why

- **The passage of real time.** AC5 and AC9 are about *the month today falls in*, and every
  observation was made on 2026-09-11. A run on 2026-10-01 would exercise the rollover, and the
  midnight race in `## Defects found` lives exactly there. What was verified instead is the rule
  at both sides of its boundary on the day it was run, plus `dates.this_month()` against
  `datetime.date.today()` in the unit suite. This is a limit of when the run happened, not a
  substitution: the criteria name *the month today falls in*, and today is what was used.
- **Locale and timezone.** `ADR-0006` records that `at` is UTC and `on` is the machine's local
  calendar day, so income typed late on the last evening of a month can fall in the next one east
  or west of UTC. That is a consequence of a delivered decision the ADR calls correct, no criterion
  of this item reaches it, and this machine's timezone is the only one exercised.
- **Stores this tool did not write.** Four of the stores above were seeded as JSON, because no
  command creates an envelope into the past or back-dates income, and AC3, AC7 and AC8 are about
  months that have ended. Each seed uses only the fields the delivered operations write, and the
  shape was cross-checked against a store built entirely through the commands. One seed
  (`/tmp/vfy/e.json`) puts a spend before the income that funds it, which `envel spend` would have
  refused — it makes the AC8 asymmetry visible in one row and the row's arithmetic is still
  correct, but it is not a store the tool could produce.
- **Concurrency.** Two runs at once against one store is not in scope for any criterion and was
  not tried.
