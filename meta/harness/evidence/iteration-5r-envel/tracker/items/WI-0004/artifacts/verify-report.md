# Verification report — WI-0004

Verified-commit: fdff4fba588e2ebafc128303f04367ec0cc58ee6

Every observation below was made by this execution against that commit, checked out on branch
`wi/WI-0004`, with `ENVEL_FILE` pointed at a scratch path that did not exist [src: ADR-0003].
Nothing here is taken from `artifacts/impl-report.md`; the report was read after the criteria, and
where it and this execution looked at the same thing they agree.

## Verdict

**Pass.** All thirteen acceptance criteria are met, each backed by a command run here and its
quoted output. Seven binding ADRs conform and none is violated. Seventeen invalidation entries
disposed `verified-still-true` were reopened and read against the branch head; all seventeen are
still true. No defect was found against this item, and none against any other item.

`verifying → in-review`.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | `envel new groceries; envel new fun; envel add groceries 100; envel move groceries fun 20 --on 2026-08-28`, then `cat $ENVEL_FILE` | `moved 20.00 from groceries, which now holds 80.00, to fun, which now holds 20.00` (exit 0); the store then holds `{"kind": "move", "envelope": "groceries", "cents": -2000, "on": "2026-08-28", ...}` and `{"kind": "move", "envelope": "fun", "cents": 2000, "on": "2026-08-28", ...}` | The criterion names the store under `ENVEL_FILE` as where the date is read, and that is where it was read. Both halves carry `2026-08-28`, the day given rather than `2026-09-11`, the day typed. |
| AC2 | pass | three envelopes funded `100`/`5`/`42.50`, `envel list` captured, `envel move groceries fun 20`, `envel list` captured, `diff` of the two | before: `fun  5.00` / `groceries  100.00` / `rent  42.50`; after: `fun  25.00` / `groceries  80.00` / `rent  42.50`; `diff` reports exactly two changed lines | Source down by exactly 20.00, destination up by exactly 20.00, and the third envelope's line byte-identical — the `diff` is the evidence that no other envelope moved, rather than an eyeball. |
| AC3 | pass | `envel move groceries fun 30.01` against a `groceries` holding `30.00` | stderr `groceries holds 30.00, which is less than 30.01. Nothing has been moved.`, stdout empty, exit 1; `envel list` afterwards still `groceries  30.00` | Checked **at** the boundary: one cent over is refused, and `envel move groceries fun 30` — exactly what the envelope holds — succeeds, leaving `groceries  0.00`. The message names the source and what is left in it, as the criterion requires. |
| AC4 | pass | `envel move nosuch fun 5`; `envel move groceries nosuchdest 5`; `envel move nosuch alsonosuch 5` | `there is no envelope called 'nosuch'. Nothing has been moved.` / `there is no envelope called 'nosuchdest'. Nothing has been moved.` / `there is no envelope called 'nosuch'. Nothing has been moved.` — each on stderr, exit 1 | Both sides exercised separately. The store's `entries` afterwards held only the original income entry, so nothing was moved. The third case fixes which name is reported when both are missing. |
| AC5 | pass | `envel move groceries fun 30` in one process, `envel list` in a second, then a third reading the file directly | second invocation: `fun  30.00` / `groceries  0.00`; the file holds `[('income','groceries',3000), ('move','groceries',-3000), ('move','fun',3000)]` | Each `envel` call is its own process; the later one re-read the store from disk. |
| AC6 | pass | `envel move a b 1` (no `--on`) then `envel move a b 2 --on 2020-01-01`, reading both moves out of the store | the first pair carries `on= 2026-09-11`, the second `on= 2020-01-01`; `date -u +%F` on the same box printed `2026-09-11` | Today's date was taken from the machine and compared, not assumed. |
| AC7 | pass | `envel move a b 5 --on X` for `28/8`, `08-28`, `yesterday`, `2026-8-28`, `20260828`, `2026-02-30`, then `--on 2026-08-28` | the six each exit 1 with stdout empty: `'28/8' is not a date: write it as YYYY-MM-DD, such as 2026-09-07` and so on, and `2026-02-30` gives `'2026-02-30' is not a day that exists…`; `--on 2026-08-28` succeeds | Three forms beyond the three the criterion names were tried — a single-digit month, the compact `20260828` that `date.fromisoformat` would otherwise accept, and a date of the right shape that is not a day. `envel list` afterwards showed only the one accepted move applied. |
| AC8 | pass | `envel move a b 5 --on 2026-09-12` and `--on 2027-09-11`, then `--on 2026-09-11` | `2026-09-12 is in the future. Nothing has been moved.` and `2027-09-11 is in the future. Nothing has been moved.`, each stderr, exit 1; today's own date moves the money and exits 0 | Checked **at** the boundary: tomorrow is refused and today is accepted, which is where an off-by-one in the comparison would show and a next-year example would not. |
| AC9 | pass | `envel move groceries fun 20` with `groceries` at `100.00` and `fun` at `5.00`, stdout and stderr captured separately | stdout `moved 20.00 from groceries, which now holds 80.00, to fun, which now holds 25.00`, stderr empty, exit 0 | All four things the criterion asks for are in the line — checked by substring, not by reading: `groceries`, `fun`, `20.00`, `80.00`, `25.00` all present, and `groceries` occurs before `fun`, so the line says which envelope the money left. The criterion's own claim about the reversal was exercised: `envel move fun groceries 20` restored `fun  5.00` / `groceries  100.00`. |
| AC10 | pass | `envel move groceries fun 0`; `… 0.00`; `… -5`; `… -- -5` | each stderr `a move has to be more than zero, and 0.00 is not. Nothing has been moved.` / `… and -5.00 is not…`, exit 1 | A negative amount was tried both as a bare `-5` and behind `--`, because argparse could plausibly have eaten the first. Both reach the refusal. The listing before and after the whole group is string-identical. |
| AC11 | pass | `envel move groceries groceries 5`; `envel move groceries Groceries 5`; `envel move GROCERIES groceries 5` | each stderr `groceries is both the envelope to take from and the one to put into, so there is nothing to move. Nothing has been moved.`, exit 1 | The capitalisation case is the one that matters and it was exercised in both directions. The message names the envelope by its stored spelling. Listing unchanged across all three. |
| AC12 | pass | see `## A criterion about criteria` below — one invocation per criterion AC12 names, with stdout, stderr and the exit code captured separately in the same call | tabulated below | Read against the eleven criteria it names, with an executable case behind each. |
| AC13 | pass | `envel move`; `envel move groceries`; `envel move groceries fun`; `envel move groceries fun 20 extra` | each stderr begins `usage: envel move [-h] [--on YYYY-MM-DD] from to amount` followed by `envel move: error: the following arguments are required: …` (and `unrecognized arguments: extra` for the fourth), stdout empty, exit 2 | Exit 2 is non-zero, which is what the criterion asks. The fourth case is the one that makes "a move carries no description" observable, and the extra word is an error rather than a description. `envel list` unchanged after all four. |

## A criterion about criteria

AC12 has criteria as its subject. It names them, so it is decidable; each is read below against the
behaviour this change introduces, with the test suite as the evidence for that reading rather than
as its definition.

| criterion AC12 covers | its sentence, read against the new behaviour | verdict |
|---|---|---|
| AC3 (refusal) | "refused… the message names the source envelope and what is left in it" — the refusal goes to stderr with stdout empty and exit 1 | still true |
| AC4 (refusal) | "refused with a message naming that envelope, and nothing is moved" — stderr, exit 1, store unchanged | still true |
| AC7 (refusal) | "each refused with a message, with nothing moved" — stderr, exit 1, stdout empty | still true |
| AC8 (refusal) | "refused with a message saying the date is in the future" — stderr, exit 1 | still true |
| AC10 (refusal) | "refused with a message; nothing is moved" — stderr, exit 1 | still true |
| AC11 (refusal) | "refused with a message naming that envelope" — stderr, exit 1 | still true |
| AC13 (refusal) | "print a usage message for the subcommand to stderr and exit non-zero" — stderr, exit **2**; non-zero is what the sentence asks, and AC12's own wording is "exits non-zero" rather than "exits 1", so the two do not collide | still true |
| AC1 (success) | a dated move succeeds — stdout carries the line, stderr empty, exit 0 | still true |
| AC2 (success) | the balances move — exit 0, output on stdout | still true |
| AC6 (success) | both the undated and the dated move succeed — stdout non-empty, stderr empty, exit 0 | still true |
| AC9 (success) | the success line — stdout only, stderr exactly `""`, exit 0 | still true |

**Non-intersection: none, and that is checked rather than assumed.** AC12's requirement is that
something executable exercise a named criterion's case *and* its stream and exit code *together*.
`tests/test_cli.py::Move::test_every_refusal_goes_to_stderr_and_every_success_to_stdout`
[src: tests/test_cli.py:685] does exactly that: one invocation per named criterion, asserting
`returncode`, `stderr` and `stdout` on the same `CompletedProcess`. There is therefore no criterion
to waive by name. This execution repeated the same eleven cases by hand, capturing the three
separately each time, and read the same result — the table above is those runs, not that test's.

The verdicts above are reads of the criteria's text. The test is the evidence; "the suite is green"
was not accepted as an answer, and the one place the two could have diverged — AC13's exit 2
against AC12's "non-zero" — was resolved by quoting both sentences rather than by noting that
nothing failed.

## ADR conformance

| ADR | verdict | clause quoted from its Decision | file and line, or why not engaged |
|-----|---------|--------------------------------|-----------------------------------|
| ADR-0001 | conforms | *"Two functions in `envel/money.py` are the only places the two forms meet… No other module converts between them, and no amount is ever held as a `float`"* | `envel/envelopes.py:254`, `:256`, `:258` render through `money.format_amount` and `envel/cli.py:108` parses through `money.parse_amount`. `grep -rn "float(\|/ 100\|\* 100" envel/` returns hits only in `envel/money.py:34` and `:42`, so the new operation adds no third place the two forms meet. |
| ADR-0002 | conforms | *"`entries` is append-only within a run and ordered as written. An envelope's balance is the sum of `cents` over the entries naming it"* | `envel/envelopes.py:244-249` appends two entries to a deep copy and removes or reorders nothing; measured on a store carrying all three kinds, the entry list after a move is prefix-identical to the list before it with exactly two appended. `balance` [src: envel/envelopes.py:50] is unchanged on this branch — `git diff main...HEAD -- envel/envelopes.py` deletes no line — and `envel list` reported `groceries  67.50` against a hand-computed `100 − 12.50 − 20`. `envel/store.py:11` still reads `FORMAT = 1`. |
| ADR-0003 | conforms | *"`$ENVEL_FILE`, used exactly as given, if it is set and non-empty"* | Every observation in this report was made with `ENVEL_FILE` set to a path that did not exist and the file appeared there; `envel/cli.py:86` reaches the store through `store.store_path()` and the new branch adds no path handling of its own. |
| ADR-0004 | conforms | *"there are two ways to start it, both reaching the same `main`: `python3 -m envel …`… `./bin/envel …`"* | The subcommand this change adds is reached through the same `main` from both: `envel/cli.py:103` is the dispatch branch and `envel/cli.py:57` the subparser, and both entry points import that `main` unchanged — `bin/envel:9` and `envel/__main__.py:5`. Both were run against it here: `python3 -m envel move a b 3` → `moved 3.00 from a, which now holds 7.00, to b, which now holds 3.00` (exit 0), and `python3 bin/envel move b a 1` → exit 0. The change adds no install step and no dependency. |
| ADR-0005 | conforms | *"`commands.test`: `python3 -m unittest discover -s tests -t .`… `commands.lint`: `python3 -m compileall -q envel tests`… every file under `envel/` and `tests/` compiles"* | Both commands were run here, exit 0 each (119 tests). The four files this change touches are all inside what those commands cover, and none imports anything third-party: `envel/envelopes.py:8-12` (`copy`, `dataclasses`, `datetime`, and the package's own `dates` and `money`), `envel/cli.py:10-13` (`argparse`, `sys`, and the package), `tests/test_cli.py:501` and `tests/test_envelopes.py:259`, the two new `Move` classes, which use `unittest`, `subprocess`, `json`, `pathlib`, `tempfile` and `datetime`. An AST walk over every file in `envel/` and `bin/envel` lists the imported modules as `argparse, copy, dataclasses, datetime, json, os, pathlib, re, sys` plus relative imports — standard library throughout. |
| ADR-0006 | conforms | *"`at` keeps the meaning `ADR-0002` gave it — when the tool recorded the entry — on every entry of every kind"* | `envel/envelopes.py:242` sets `at = now()` and writes it to both entries; `on` is a separate field at `:243`. On a store carrying all three kinds, a move written `--on 2020-01-01` carries `at= 2026-09-11T06:00:32Z`, so the event date did not leak into `at` on the kind the sentence did not name. |
| ADR-0007 | conforms | *"A move appends exactly two entries… `cents` carries the direction, negative on the side the money left… `on` is the day the move is held against… present on both entries of a move and they always agree… The document's `format` stays `1`"* | Read out of a real store: two entries, `{"kind":"move","envelope":"groceries","cents":-2000,"on":"2026-08-28"}` and `{"kind":"move","envelope":"fun","cents":2000,"on":"2026-08-28"}`, with the same `at` on both; `envel/envelopes.py:242-249` computes `at` and `day` once each and writes each twice; `envel/store.py:11` unchanged at `FORMAT = 1`. No `description` is written on a move entry, and no field links the pair. |

**No ADR outside the plan's list was found engaged.** The change adds one operation in
`envel/envelopes.py` and one subparser and branch in `envel/cli.py`; there are seven ADRs in
`docs/architecture/adr/` and all seven are on the plan's list, so there was none left to be
missed. No verdict here is `violates` and none is `not-engaged`.

## Invalidation set

Nineteen entries. Seventeen disposed `verified-still-true` were reopened and read against the
branch head; one disposed `to-update` was checked for the update it claims; two disposed
`owned-by-ending` were left exactly as they are. **This execution wrote nothing under `docs/`** —
`git status` is clean apart from this report and the ticked criteria.

| document | disposition | what I reopened, and what I found |
|----------|-------------|-----------------------------------|
| `docs/architecture/overview.md` `## The parts`, the `envel/envelopes.py` row | verified-still-true | The row says the module owns *"create, add income, list, record a spend, move money between two envelopes"* — five. `grep -n "^def " envel/envelopes.py` gives nine functions, of which `now`, `fold`, `find` and `balance` are helpers and five are operations: `create:58`, `add_income:78`, `record_spend:108`, `listing:171`, `move:184`. Exactly the five named, in that module. **Still true.** |
| `docs/architecture/overview.md` `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | verified-still-true | Quantified, so enumerated: the modules below `cli` are `envelopes`, `store`, `money` and `dates` — the four the dependency sentence names and the four `envel/cli.py:13` imports. `grep -n "print(\|sys.exit\|sys\.std" envel/envelopes.py envel/store.py envel/money.py envel/dates.py` exits 1 with no hits. The falsifier is a `print` or `sys.exit` in a function the sentence does not name, and the new `move` is exactly such a function — it returns `Ok` or `Refusal` as a value [src: envel/envelopes.py:250], and `envel/cli.py:120` is what prints it. **Still true.** |
| `docs/architecture/overview.md` `## The data`, the move sentences | verified-still-true | The document says two entries of kind `move`, one naming each envelope, `cents` negative where the money left and positive where it arrived, the same `on` and the same `at` on both, and *"Nothing in the file links the two halves of a move to each other"*. Read off a real store: `-2000`/`groceries` and `2000`/`fun`, `on` `2026-08-28` on both, `at` equal on both, and the field sets of the two entries are `{kind, envelope, cents, on, at}` — no identifier, nothing linking them. **Still true.** |
| `docs/architecture/overview.md` `## The data`: *"a balance is the sum of an envelope's entries rather than a stored number"* | verified-still-true | Quantified. The falsifier is an entry kind `balance` has to special-case, and `move` is the first new kind since a spend — so the check was made on a store holding **all three** kinds at once (income `10000`, spend `-1250` dated `2026-09-01`, move `-2000` dated `2020-01-01`), not on the happy path of a fresh store. Summing `cents` by folded envelope name with no branch on `kind` gives `6750` and `2000`; `envel list` printed `groceries  67.50` and `fun  20.00`. Identical, so nothing is stored and nothing is special-cased. **Still true.** |
| `docs/architecture/overview.md` `## Conventions…`: *"A date typed at the command line is written `YYYY-MM-DD` and nothing else"* | verified-still-true | Quantified over the command-line date inputs, so they were enumerated: `grep -n '"--on"' envel/cli.py` returns two, line 50 (`spend`) and line 66 (`move`), and there is no other date-shaped argument in the parser. Both were tried with a form that is not `YYYY-MM-DD`: `envel spend groceries 1 --on 28/8` and `envel move groceries fun 1 --on 28/8` each exit 1 with `'28/8' is not a date…`, and so do `--on 20260828` on a spend and `--on 2026/08/28` on a move. The falsifier is an input this change adds that takes some other form; the input it adds is line 66 and it does not. **Still true.** |
| `docs/architecture/overview.md` `## What is not decided yet`, now naming three items | verified-still-true | The sentence names `WI-0003`, `WI-0005` and `WI-0006` and says moving money *"has left this list: it is `ADR-0007`… for `WI-0004`"*. The board carries six work items; `WI-0001` and `WI-0002` are `done`, `WI-0004` is this one, and the remaining three are exactly those named. `ADR-0007` exists and is `status: current`. The sentence also claims the remaining three build on `ADR-0002` *"without changing the file's shape"*, whose falsifier would be a `format` change — `envel/store.py:11` still reads `FORMAT = 1`. **Still true.** |
| `docs/architecture/overview.md` `## Engagement state` | owned-by-ending | Left exactly as it is, and confirmed untouched: no commit matching `WI-0004` edits it (`git log --grep WI-0004` names five workspace commits and one, the plan's, touches `overview.md` — its change-log row covers `## The parts`, `## The data` and `## What is not decided yet`, and the section still reads *"`WI-0001` is the first item to be designed"*, which is the stale sentence the ending owns). Not repaired here. |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` — `## Decision`, the JSON pair and the six bullets | verified-still-true | Checked field for field and sign for sign against a store this execution wrote; the comparison is the ADR-0007 row of `## ADR conformance` above. **Still true.** |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` — `## Decision`: *"The document's `format` stays `1`"* | verified-still-true | `envel/store.py:11` is `FORMAT = 1`; the only three uses are the initial document `:30`, the load check `:54` and its message `:57`, and nothing branches on any other value. The branch diff touches `envel/store.py` not at all. **Still true.** |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` — `## Consequences`: *"the tool gains one entry kind and no field that some other kind does not already carry"* | verified-still-true | Quantified, so enumerated from a store holding every kind the tool writes: `income` → `{at, cents, envelope, kind}`, `spend` → `{at, cents, description, envelope, kind, on}`, `move` → `{at, cents, envelope, kind, on}`. The falsifier is a field on a `move` entry that no other kind carries; the set difference of `move`'s fields against the union of the others is **empty**. **Still true.** |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` — `## Decision`: *"`at` keeps the meaning… on every entry of every kind"* | verified-still-true | Quantified over kinds, and the kinds are three. Checked at the case that could falsify it rather than the easy one: a move written `--on 2020-01-01`, six years before the run, carries `at= 2026-09-11T06:00:32Z` — the recording moment, not the event. The spend in the same store, dated `2026-09-01`, does the same; income carries `at` and no `on`. **Still true.** |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` — `## Consequences`: the enumeration of the sums `WI-0003` makes | to-update | Named a document that was actually updated. `ADR-0006` is at `version: 2`, `updated-by: implement`, `updated-for: WI-0004`, with a change-log row for version 2 and a `## Corrections` row recording the erratum. The sentence now reads *"sums a month's spending by `on`, a month's moves by `on` [src: ADR-0007], and a month's income by `at`"* — three clauses for three kinds. The surviving clause *"with no branch on what a date means"* was read against the branch: `on` is the day it happened on both a spend [src: envel/envelopes.py:150] and a move [src: envel/envelopes.py:245], so it holds. |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — `## Decision`: *"An envelope's balance is the sum of `cents` over the entries naming it"* | verified-still-true | Same enumeration as the overview's balance row, and the same three-kind store. `balance` is unchanged on this branch and needs no branch on `kind`. **Still true.** |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — `## Decision`: *"`entries` is append-only within a run and ordered as written"* | verified-still-true | The falsifier is a rewritten or reordered existing entry, and this change is the first to append **two** at once — so the entry list was captured before a move and compared after: the first two elements are identical objects in the same order and exactly two were appended, in the order source-then-destination. Nothing in `move` deletes, sorts or mutates an existing entry; it deep-copies and appends [src: envel/envelopes.py:239-249]. **Still true.** |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` — `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | verified-still-true | Quantified over the whole tool. `grep -rn "parse_amount\|format_amount\|float(\|/ 100\|\* 100" envel/ --include=*.py` returns the two definitions at `money.py:20` and `:38`, the arithmetic at `money.py:34` and `:42`, and nothing but call sites elsewhere. The falsifier would be a conversion in the new code; `move` formats through `money.format_amount` at four call sites and the cli branch parses through `money.parse_amount` at `cli.py:108`. **Still true.** |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` — `## Decision`, the two commands and what lint checks | verified-still-true | Both commands were run by this execution against the branch head: `python3 -m unittest discover -s tests -t .` → exit 0, 119 tests; `python3 -m compileall -q envel tests` → exit 0. The four files this change touches are two under `envel/` and two under `tests/`, all inside what those commands cover. **Still true.** |
| `docs/product/vision.md` `## What it is for`: the moving-money sentences | verified-still-true | *"moving an amount from one envelope to another"* now describes delivered behaviour and matches it: `envel move <from> <to> <amount>`. The sentence's reason — *"Moving money is what they want to do when an envelope runs short, because they chose to have an overspend refused rather than shown as a negative envelope"* — was checked rather than assumed: `envel spend groceries 1000` against `67.50` still gives `groceries holds 67.50, which is less than 1000.00. Nothing has been recorded; move money into it first if you want to spend that.` and exit 1, and the listing shows no negative envelope. **Still true.** |
| `docs/product/vision.md` `## What it deliberately is not`, bullet 2 | verified-still-true | *"no server, no sync, no bank import, no network."* Quantified, and the falsifier would be a module the sentence does not name — so the imports were enumerated rather than eyeballed: an AST walk over every file in `envel/` and `bin/envel` gives `argparse, copy, dataclasses, datetime, json, os, pathlib, re, sys` plus the package's relative imports. Intersected with the network-capable standard-library modules (`socket, http, urllib, ssl, ftplib, smtplib, asyncio, subprocess`): **empty**. **Still true.** |
| `docs/product/vision.md` `## Engagement state` | owned-by-ending | Left exactly as it is. No `WI-0004` commit touches `vision.md`; the section still says the engagement has just begun and `EP-001` is suspended, which is stale and is the ending's to restate. Not repaired here. |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 119 tests … OK`, run by this execution on `fdff4fb` |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | pass | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | pass | `## Criteria` — thirteen rows, each with a command this execution ran and its quoted output. The implementation report is cited nowhere as evidence. |
| `negative-cases-exercised` | pass | `## Negative and boundary cases exercised` |
| `a-criterion-about-criteria-is-read` | pass | `## A criterion about criteria` — AC12's eleven named criteria, one verdict each, non-intersection checked and absent |
| `adr-conformance-is-decided` | pass | `lint-documents --rule adr-conformance-is-decided --item WI-0004` → exit 0, over `## ADR conformance` |
| `invalidation-set-is-disposed` | pass | `lint-documents --rule invalidation-set-is-disposed --item WI-0004` → exit 0, over `## Invalidation set` |
| `tests-would-fail-without-the-change` | pass (advisory) | `## Test sensitivity check` — thirteen mutations, one per criterion, each making the named test fail |

## Negative and boundary cases exercised

Every one of these was triggered here, not read about.

- **AC3, at the boundary.** `30.01` against a `30.00` envelope is refused; `30.00` exactly is
  allowed and empties the envelope. An off-by-one in the comparison would show here and nowhere
  else.
- **AC4, both sides and both missing.** Missing source, missing destination, and both missing at
  once — the last fixes that the source is the one reported.
- **AC7, six malformed dates.** The three the criterion names (`28/8`, `08-28`, `yesterday`) plus
  `2026-8-28` (single-digit month), `20260828` (the compact ISO form `date.fromisoformat` accepts
  and this tool must not) and `2026-02-30` (right shape, not a day). Each exits 1 with stdout
  empty; the listing is unchanged; `2026-08-28` is then accepted.
- **AC8, at the boundary.** Tomorrow, computed from the machine's clock, is refused; today is
  accepted. Next year was tried too, but it is the tomorrow/today pair that decides the comparison.
- **AC10, zero and negative, and the argparse trap.** `0`, `0.00`, `-5`, and `-- -5`, because a
  bare `-5` could plausibly have been swallowed as an option before reaching the refusal. All four
  refuse; the listing is string-identical before and after the group.
- **AC11, both capitalisations.** `groceries → groceries`, `groceries → Groceries` and
  `GROCERIES → groceries`. The middle one is the case that matters, since the destination resolves
  through case-folding to the same envelope.
- **AC13, all four wrong argument counts**, each checked for the subcommand's own usage line rather
  than the tool's, and each leaving the listing unchanged.
- **An empty store.** Every scratch run began with `ENVEL_FILE` pointing at a path that did not
  exist, so the store's creation is exercised on every one of them.
- **A store carrying all three entry kinds at once**, used for the invalidation audit — the case a
  fresh-store check would miss.

## Test sensitivity check

Thirteen mutations, one per criterion, each applied to the branch head, the named test run, and
the source restored. The two source files were compared byte-for-byte with their originals
afterwards and `git status` is clean.

| AC | mutation | named test | result |
|----|----------|------------|--------|
| AC1 | the source entry's `on` written as `"1999-01-01"` | `Move.test_a_dated_move_is_held_against_that_date` | failed |
| AC2 | the destination entry's `cents` halved | `Move.test_only_the_two_named_envelopes_move` | failed |
| AC3 | `if cents > remaining:` → `if False:` **in `move`** | `Move.test_more_than_the_source_holds` | failed |
| AC4 | the missing-source message stripped of the name | `Move.test_an_envelope_that_does_not_exist_on_either_side` | failed |
| AC5 | `changed=True` → `changed=False`, so nothing is saved | `Move.test_a_move_survives_into_a_later_invocation` | failed |
| AC6 | the cli branch always parsing `"2020-01-01"` | `Move.test_no_date_given_records_today_and_a_date_given_is_kept` | failed |
| AC7 | the cli branch ignoring `--on` and always using today | `Move.test_only_the_full_form_of_a_date_is_accepted` | failed |
| AC8 | `if on > dates.today():` → `if False:` **in `move`** | `Move.test_a_date_in_the_future_is_refused_and_today_is_not` | failed |
| AC9 | the success line replaced with a bare `moved money` | `Move.test_the_line_names_both_envelopes_the_amount_and_what_each_holds` | failed |
| AC10 | `if cents <= 0:` → `if False:` **in `move`** | `Move.test_zero_and_negative_amounts` | failed |
| AC11 | the same-envelope guard → `if False:` | `Move.test_the_same_envelope_on_both_sides` | failed |
| AC12 | `envel/cli.py` printing a refusal to stdout instead of stderr | `Move.test_every_refusal_goes_to_stderr_and_every_success_to_stdout` | failed |
| AC13 | `if unrecognised:` → `if False:` in `envel/cli.py` | `Move.test_the_wrong_number_of_words` | failed |

**Three of these looked insensitive on the first attempt, and the harness was wrong rather than
the tests.** `record_spend` carries the same three guard lines as `move` — `if cents <= 0:`,
`if on > dates.today():` and `if cents > remaining:` — so a textual replace-first mutated the
spend's copy and left the move's intact, and the move test passed because the move's behaviour was
never removed. This was caught by running the mutant by hand (`envel move groceries fun 100`
against a `40.00` envelope still refused) rather than by trusting the harness's verdict, and the
three were redone against `move`'s own line numbers, where all three fail. Recording it because the
first result is the shape of a real finding and was not one; a reader should not have to re-derive
why the numbers moved.

## Defects found

**None.** No criterion of this item failed, so there is no send-back. No behaviour delivered by
another item was found broken, so no bug item was filed.

Two cross-item checks were made deliberately, because adding a subcommand is where a delivered
criterion of another item quietly becomes false:

- `WI-0001` AC14 — the tool's usage message lists the subcommands it has. `python3 bin/envel` with
  no subcommand prints `usage: envel [-h] {new,add,list,spend,move} …` to stderr: five listed,
  five in the parser. Not falsified.
- `WI-0002` — the spend path is untouched by this change and still behaves: an overspend is
  refused with the spend's own message, and `envel spend --on 28/8` is still rejected.

## Not verified, and why

- **That a move's `at` is computed once and written twice rather than twice and coincidentally
  equal.** This execution observed the two halves carrying the same `at` on every move it made,
  which is what `ADR-0007` asks for, but the clock's resolution is one second and both writes fall
  in the same second — so the observation cannot distinguish one computation from two. It is
  settled by reading `envel/envelopes.py:242`, where `at = now()` is bound once before either
  append, and by `tests/test_envelopes.py`, which the implementation report records as installing a
  clock returning a different value per call for exactly this reason. No acceptance criterion of
  this item depends on it; it is declared here because the evidence for it is a read and a test
  rather than an observation this execution could make.
- **What `WI-0003` will do with `move` entries.** This item stores them so that a month's net moved
  figure can be summed with a filter; nothing computes that figure yet, and no criterion of this
  item asks for it. The shape was checked against `ADR-0007` and against the sentence `WI-0003` AC2
  already carries, and that is as far as it can be checked before `WI-0003` is built.
- **A move's date shown back to a person.** Nothing this item delivers prints one, which is why
  AC1 and AC6 name the store file as the place it is observed. Verified there; a rendering of it
  cannot be verified because there is none.
- **Behaviour on a store whose `format` is not `1`, and on a damaged file.** Out of scope for this
  item: `ADR-0002` and `WI-0001` own it, and `envel/store.py` is untouched by this change.
- **Any criterion of another item beyond the two cross-checks named above.** `WI-0001` and
  `WI-0002` were verified when they were delivered; this execution re-checked only the two places
  adding a subcommand could plausibly have broken them.
