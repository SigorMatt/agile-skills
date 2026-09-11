# Verification report — WI-0001

Verified-commit: 2f025c5c45b039c8c563bcbc46884e3e8b14efc4

This is the **second** verification of `WI-0001`. The first, at commit `26d25ce`, passed sixteen
criteria and failed AC15, and sent the item back to `in-progress`. That report is in this file's
git history (`git show HEAD~2:tracker/items/WI-0001/artifacts/verify-report.md`); this one
replaces it rather than appending to it, because a verification is a statement about one commit
and two of them in one file is two statements about different code.

**Nothing was carried over on trust.** The first report warned that AC14 and AC16 come from the
same code path as AC15 and should be treated as unverified after any fix. In the event the whole
of the seventeen was re-run against the new head, not just those three: the change is in
`envel/cli.py`'s entry point, which every criterion goes through.

## Verdict

**Pass. All seventeen criteria are met, on evidence gathered here.**

AC15 is fixed. All five invocations the criterion names now print a usage message for the
subcommand that was misused — `usage: envel new [-h] name`, `usage: envel add [-h] name amount`,
`usage: envel list [-h]` — and AC14 still prints the tool's own usage listing all three
subcommands, which is the case AC15 is deliberately the opposite of. The two are now pinned apart
by assertions in opposite directions, so neither can drift into the other silently.

The advisory gate that failed last time now passes: fourteen mutations were tried against the new
head and **all fourteen** turn the suite red, including the two that previously did not.

No defect was found. No bug item was filed.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | `ENVEL_FILE=/tmp/vrf2/a.json bin/envel new groceries` | stdout `created envelope groceries`, stderr empty, exit 0 | contains the name, says it was created |
| AC2 | pass | `bin/envel add groceries 400` | stdout `added 400.00 to groceries, which now holds 400.00`, stderr empty, exit 0 | contains the name and the amount now in it |
| AC3 | pass | after creating `groceries`, `Zebra`, `apple`, `eating out`: `bin/envel list` | stdout `apple  0.00` / `eating out  0.00` / `groceries  410.00` / `Zebra  0.00`, exit 0 | one line per envelope, name and amount, no total line, nothing else. `Zebra` sorts last rather than first, so the order ignores capitalisation rather than comparing bytes |
| AC4 | pass | `new groceries`, `add groceries 400`, `list` as three separate `bin/envel` processes on one `ENVEL_FILE` | the third prints `groceries  400.00`, exit 0 | each process exited before the next started; nothing else ran between them |
| AC5 | pass | `bin/envel add nosuch 10`, then `bin/envel list` | stderr `there is no envelope called 'nosuch'. Nothing has been changed.`, stdout empty, exit 1; the listing afterwards is `groceries  400.00` with no `nosuch` line | names the envelope; nothing created as a side effect |
| AC6 | pass | `ENVEL_FILE=/tmp/vrf2/a.json bin/envel list` against a path that does not exist | stdout `no envelopes yet`, exit 0; `ls` afterwards: `No such file or directory` | a line saying there are none, and the read creates nothing |
| AC7 | pass | with `groceries` holding 400.00: `bin/envel new groceries`, then `bin/envel list` | stderr `there is already an envelope called 'groceries', holding 400.00. Nothing has been changed.`, stdout empty, exit 1; the listing still reads `groceries  400.00` | refused, names it, says it exists, and the money is intact |
| AC8 | pass | `add g 12.5`; `add g 12.567`; `add g 12.57` | `12.5` → `added 12.50 to g, which now holds 12.50`, exit 0. `12.567` → stderr `'12.567' has more than two decimal places: an amount is written with at most two`, exit 1, and the following listing is unchanged at `g  12.50`. `12.57` → `added 12.57 to g, which now holds 25.07` | `12.5` means 12.50; three places refused with nothing recorded; two decimal places always printed, including the cent digit that is not a round ten |
| AC9 | pass | `bin/envel add pennies 0.01` × 100 separate processes, then `bin/envel list` | stdout `pennies  1.00`, exit 0; the store holds 100 entries | one hundred separate invocations, one hundred entries on disk, exactly `1.00`. And separately `12.57 + 0.03` across two invocations listed as `25.07`, so nothing is lost at the cent either |
| AC10 | pass | `add g 0`; `add g -40`; then `list` | `0` → stderr `income has to be more than zero, and 0.00 is not. Nothing has been changed.`, exit 1. `-40` → the same with `-40.00`, exit 1. The listing is unchanged at `g  25.07` | both refused, amount unchanged. The negative is refused as income, not as a malformed number — the split AC17 asks for |
| AC11 | pass | `new groceries`, `add Groceries 10`, `new GROCERIES`, `list` | the add succeeds reporting `groceries`; `new GROCERIES` → stderr `there is already an envelope called 'groceries', holding 410.00`, exit 1; the listing shows one `groceries` line | capitalisation reaches the same envelope, and AC7's refusal fires for the same reason |
| AC12 | pass | the same sequence, then `bin/envel list` | the line reads `groceries  410.00` | shown as first typed, after being referred to as `Groceries` and `GROCERIES` |
| AC13 | pass | `new "eating out"`; `new "car & bike"`; `new ""`; `new " x"`; `new "x "`; then `list` | the first two exit 0 and both appear in the listing. `""` → stderr `an envelope needs a name. Nothing has been created.`, exit 1. `" x"` and `"x "` → stderr `'…' begins or ends with a space, which an envelope name may not.`, exit 1, and neither is listed | spaces and punctuation accepted; empty and both edge cases refused. Both edges checked, not only the leading one |
| AC14 | pass | `bin/envel` with no arguments; `bin/envel frobnicate`; then `ls $ENVEL_FILE` | both → stderr `usage: envel [-h] {new,add,list} ...` on the first line, stdout empty, exit 2; the store file does not exist afterwards | **re-checked rather than assumed**, because the fix for AC15 is in the same function. The usage is still the *tool's*, still lists all three subcommands, and nothing is created or changed |
| AC15 | **pass** | the five invocations the criterion names: `new`; `new a b`; `add groceries`; `add groceries 10 20`; `list extra` | `new` → `usage: envel new [-h] name`. `new a b` → `usage: envel new [-h] name` / `envel new: error: unrecognized arguments: b`. `add groceries` → `usage: envel add [-h] name amount`. `add groceries 10 20` → `usage: envel add [-h] name amount` / `envel add: error: unrecognized arguments: 20`. `list extra` → `usage: envel list [-h]` / `envel list: error: unrecognized arguments: extra`. All five: stdout empty, exit 2, and the listing afterwards unchanged at `groceries  50.00` | **The defect is gone.** All five print a usage message *for that subcommand*; none prints the top-level `{new,add,list}` line. The three that failed last time were `new a b`, `add groceries 10 20` and `list extra`, and all three were re-run here |
| AC16 | pass | every criterion it names, re-run with the three channels captured separately — see `## A criterion whose subject is other criteria` | every refusal: stderr non-empty, stdout empty, exit non-zero. Every success: stdout non-empty, stderr empty, exit 0 | eleven per-criterion verdicts below. The non-intersection the last report recorded is closed |
| AC17 | pass | `add g 400`, `add g 12.5`, `add g 12.50` accepted; `add g '£12.50'`, `add g '1,200'`, `add g 12.5x`, `add g abc` refused; every printed amount inspected | the accepted forms exit 0. Each refused form → stderr `'…' is not an amount: write a plain number such as 12.50, with no currency symbol and no thousands separator`, exit 1, listing unchanged. No amount printed in any run in this report carries a currency symbol | `-40` is still refused by AC10's message rather than this one |

## A criterion whose subject is other criteria

AC16 names eleven criteria by ID: *"Every refusal this item specifies writes its message to stderr
and exits non-zero, and every command that succeeds writes its output to stdout and exits 0.
Checked case by case against the criteria that name them: refusals at AC5, AC7, AC8, AC10, AC13,
AC14 and AC15; successes at AC1, AC2, AC3 and AC6."*

Read against the new behaviour, one criterion at a time, from runs made for this section:

| criterion named by AC16 | the case run | stdout | stderr | exit | verdict |
|---|---|---|---|---|---|
| AC5 refusal | `add nosuch 10` | empty | the message | 1 | still true |
| AC7 refusal | `new groceries` on a taken name | empty | the message | 1 | still true |
| AC8 refusal | `add g 12.567` | empty | the message | 1 | still true |
| AC10 refusal | `add g 0`, `add g -40` | empty | the message | 1 | still true |
| AC13 refusal | `new ""`, `new " x"`, `new "x "` | empty | the message | 1 | still true |
| AC14 refusal | `envel`, `envel frobnicate` | empty | the **tool's** usage | 2 | still true |
| AC15 refusal | the five invocations | empty | the **subcommand's** usage | 2 | still true |
| AC1 success | `new groceries` | the line | empty | 0 | still true |
| AC2 success | `add groceries 400` | the line | empty | 0 | still true |
| AC3 success | `list` with envelopes | the lines | empty | 0 | still true |
| AC6 success | `list` with none | `no envelopes yet` | empty | 0 | still true |

No sentence of AC16 is falsified by the change. AC15's messages moved from the tool's parser to
the subcommands' parsers; the *stream* and the *exit code* — the only things AC16 asserts — did
not move, and both were observed rather than inferred.

**The non-intersection the last report declared is now closed, and closed the way it asked.** It
recorded, in those words, that *nothing executable exercises AC15's "a usage message for that
subcommand" clause and AC16's stream-and-exit-code rule together*, because
`test_the_wrong_number_of_arguments` reduced AC15 to `assertTrue(run.stderr.strip())` — AC16's
claim. It now asserts three further things per invocation: that the first line of stderr starts
`usage:`, that it names the subcommand, and that it does **not** contain `{new,add,list}`. Its
counterpart `test_no_subcommand_and_an_unknown_one` asserts the opposite for AC14. I confirmed
both assertions bite, by mutation rather than by reading them:

- reverting `parse_known_args` back to `parse_args` fails `test_the_wrong_number_of_arguments`
  and nothing else — a precise, single-criterion failure, which is what AC15 having its own
  covering case means;
- routing AC14's failures through a subcommand parser fails sixteen tests including
  `test_no_subcommand_and_an_unknown_one`.

No waiver is claimed, because no covering case is missing.

AC16's enumeration remains narrower than its own first sentence: *"every refusal this item
specifies"* includes AC17's, and the list of IDs omits AC17. Checked anyway rather than left:
`add g '£12.50'`, `'1,200'`, `12.5x` and `abc` each put the message on stderr with stdout empty
and exit 1, so the universal sentence holds too. An observation about AC16's wording, not a
defect — the same one the first report made, unchanged by this round.

## ADR conformance

| ADR | verdict | clause quoted from its Decision | file and line, or why not engaged |
|-----|---------|--------------------------------|-----------------------------------|
| `ADR-0001` | conforms | *"Two functions in `envel/money.py` are the only places the two forms meet … No other module converts between them, and no amount is ever held as a `float` or written to the store as a decimal string."* | `envel/money.py:20` (`parse_amount`) and `envel/money.py:38` (`format_amount`). `grep -rn "float(\|Decimal\|round(" envel/` returns nothing. Every other mention is a call into those two — `envel/envelopes.py:71,83,99,101,114` and `envel/cli.py:61` — and none converts for itself. The store holds `"cents": 500`, an integer, read back from a store this verification wrote. Untouched by this round's change, and re-read against the new head rather than carried over |
| `ADR-0002` | conforms | *"`format` is an integer this tool checks on load … An envelope's balance is the sum of `cents` over the entries naming it … Writes are atomic … moved over the target with `os.replace` … A missing file is an empty store … A file that exists but cannot be read as this format … is refused … and **nothing is written**"* | The document written by the new head is field for field the ADR's: `{"format": 1, "envelopes": [{"name","created"}], "entries": [{"kind","envelope","cents","at"}]}`. `envel/store.py:80` is the `os.replace`, `envel/store.py:77` the temporary beside the target, `envel/store.py:75` the parent-directory creation on write. `envel/envelopes.py:50` derives the balance; the envelope record carries no balance field. Missing file → `no envelopes yet`, exit 0, nothing created. `not json` → exit 1 and `cat` afterwards still reads `not json`. `format: 99` → exit 1, file intact |
| `ADR-0003` | conforms | *"1. `$ENVEL_FILE`, used exactly as given, if it is set and non-empty; 2. otherwise `$XDG_DATA_HOME/envel/envelopes.json` …; 3. otherwise `~/.local/share/envel/envelopes.json`. Missing parent directories are created when the store is first written, and never on a read."* | `envel/store.py:18`. All three branches exercised on the new head: `ENVEL_FILE` set *beside* `XDG_DATA_HOME` → the file appeared at `/tmp/vrf2/h.json`; `XDG_DATA_HOME` alone → `/tmp/vrf2/xdg/envel/envelopes.json`, parents created on the write; neither set → `store_path()` returned `/home/msi/.local/share/envel/envelopes.json`, and being a read it wrote nothing there |
| `ADR-0004` | conforms | *"there are two ways to start it, both reaching the same `main`: `python3 -m envel …`, via `envel/__main__.py`; `./bin/envel …`, an executable file whose body puts the repository root on `sys.path`, imports `envel.cli.main` and calls it under `sys.exit`"* and *"No third-party packaging or dependency is introduced"* | `envel/__main__.py:5` and `bin/envel:9`. **This is the ADR this round's change could most plausibly have broken**, because `build_parser` now returns a tuple and `main`'s first statements changed, so both entry points were re-run — on a success path (`list` → both gave `tools  5.00`, exit 0) **and on the failure path that changed** (`list extra` → both gave `usage: envel list [-h]` / `envel list: error: unrecognized arguments: extra`, exit 2). Byte-identical in both directions. No `pyproject.toml`; every import across the seven files is standard library or intra-package |
| `ADR-0005` | conforms | *"`commands.test`: `python3 -m unittest discover -s tests -t .` … `commands.lint`: `python3 -m compileall -q envel tests`"* | `tracker/project.yaml:14` and `tracker/project.yaml:15` carry those two strings character for character. Run here on the new head: test → exit 0, 52 tests, OK; lint → exit 0. No third-party dependency was added by this round — the change uses `argparse`, which was already imported at `envel/cli.py:10` |

No ADR outside the plan's binding list was found engaged. In particular the change touches no
decision about storage, amounts or invocation: it is confined to which parser reports an
argument-shape failure, and no ADR speaks to that.

## Invalidation set

The set is the plan's, and it was closed by the first implementation. The second execution wrote
no document, so no entry changed hands. Each row was nevertheless **re-read against the new
branch head**, because a disposition is a claim about code and the code moved.

| document | disposition | what I reopened, and what I found |
|----------|-------------|-----------------------------------|
| `docs/product/vision.md` — `## Engagement state` bullet 1 | owned-by-ending | Left as it is. `git diff --name-only 26d25ce..HEAD -- docs/` is **empty**, so this round touched no document at all, let alone one the ending owns |
| `docs/product/vision.md` — `## Engagement state` bullet 2 | owned-by-ending | Same; confirmed unedited by the same check |
| `docs/product/vision.md` — `## What it is for`: *"The command is `envel`"* | verified-still-true | **Reopened and true.** `bin/envel` exists, and the parser is still built with `prog="envel"` at `envel/cli.py:23` — which is what every usage message in this report prints, on both the tool's line and the subcommands'. The change made the sentence *more* visible, not less true |
| `docs/product/vision.md` — `## What it deliberately is not`: *"Not connected to anything: no server, no sync, no bank import, no network."* | verified-still-true | **Reopened and true.** Quantified, so the enumeration. **Set:** the seven files that are the tool (`ls envel/*.py bin/envel`). **Enumerated with** `grep -n "^import \|^from \|^\s*import \|^\s*from " envel/*.py bin/envel` → 16 lines on the new head: `argparse`, `sys`, `copy`, `dataclasses`, `datetime`, `pathlib`, `re`, `json`, `os`, plus the intra-package imports. **Verdict per member:** none is a network module. **Falsifier:** a `socket`, `urllib`, `http`, `ssl`, `asyncio` or `requests` import in any of the seven; `grep -rnE` over all of them returns no match. The grep reads every import unfiltered, so it is the command that would have shown one |
| `docs/architecture/overview.md` — `## The parts`, the module table | to-update | **Updated in the first execution; still right after this one.** Six rows, six files, all present. The row for `envel/cli.py` reads *"the command line: parsing arguments, dispatching, printing, and the exit code"* — still exactly what it does, and the only module that parses arguments. Version 2, change-log row at `2026-09-11T02:43:44Z`. No further bump was owed because nothing became false |
| `docs/architecture/overview.md` — `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | verified-still-true | **Reopened and true, and this round is the one that could have broken it.** The fix adds an error path, and the tempting place to put it would have been in a lower module. It is not: `subcommand_parsers[...].error(...)` is at `envel/cli.py:51`, inside `cli`. **Set:** `envel/money.py`, `envel/store.py`, `envel/envelopes.py`. `grep -n "print(\|sys\.exit\|sys\.stdout\|sys\.stderr\|\.write(\|write_text"` over the three returns exactly one line, `envel/store.py:77` `temporary.write_text(` — **checked at the boundary rather than the happy path**, and a write to a *file* is not what the sentence forbids |
| `docs/architecture/overview.md` — `## The data`: *"a balance is the sum of an envelope's entries rather than a stored number"* | verified-still-true | **Reopened and true.** `envel/envelopes.py:50` sums the entries and is what the listing calls. The falsifier is a stored balance; the envelope record in a store written by the new head has keys `created` and `name` only, and the document's top level is `entries`, `envelopes`, `format` |
| `docs/architecture/overview.md` — `## Engagement state` | owned-by-ending | Left alone; confirmed unedited |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` — *"Two functions … are the only places the two forms meet"* | verified-still-true | **Reopened and true.** **Set:** the seven files. **Enumerated with** `grep -rn "float(\|Decimal\|round(" envel/` → nothing, and `grep -rn "format_amount\|parse_amount" envel/` outside `money.py` → six lines, every one a call. **Boundary:** the nearest a module comes to converting is `envel/envelopes.py`, which builds messages containing amounts at `:71, :83, :99, :101, :114` — exactly where a hand-written `"%.2f"` would sit — and all five delegate |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — the JSON document and the atomic write | verified-still-true | **Reopened and true.** Covered field for field in the ADR-0002 conformance row above, from a store this verification wrote and read back on the new head |
| `docs/architecture/adr/ADR-0003-store-location.md` — the three-step resolution | verified-still-true | **Reopened and true.** All three branches exercised; see the ADR-0003 row |
| `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` — the two entry points | to-update | **Updated in the first execution; re-read here because this round changed `main`'s signature and first statements.** The corrected text names `bin/envel` and the `sys.path` line, both of which are still there, and both entry points were re-run on a success and a failure path with identical results. Version 2 with a change-log row and a `## Corrections` entry quoting the removed clauses |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` — *"The test command exits 5 while no test exists"* | verified-still-true | **Reopened and true, at its boundary.** The sentence predicts its own expiry — *"becomes exit 0 as soon as `implement` writes the first test"*. Both halves hold simultaneously: a fresh directory with only `tests/__init__.py` gives `NO TESTS RAN`, exit 5; this repository gives exit 0 on 52 tests |
| `docs/product/vision.md` — *"the tool starts, does one thing, and exits … nothing runs between invocations"* | verified-still-true | **Reopened and true.** **Set:** the same seven files. **Enumerated with** `grep -n "threading\|multiprocessing\|subprocess\|atexit\|signal\|daemon\|fork\|Popen" envel/*.py bin/envel` → no match. **Falsifier:** anything outliving a process — a thread, an `atexit` handler, a forked child. The behavioural evidence is the AC9 run: a hundred processes started and exited, and the only thing carrying state between them was the file, which held exactly a hundred entries |

All fourteen entries carry a disposition. **I wrote no file under `docs/`**, and this round's
implementation did not either — `git diff --name-only 26d25ce..HEAD -- docs/` is empty.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → `Ran 52 tests … OK`, exit 0, run here on `2f025c5` |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0, run here |
| `workspace-valid` | pass | `validate-workspace` → 7 items, 7 documents, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | pass | `## Criteria`: seventeen rows, each with a command this execution ran against `2f025c5` and its actual output. None cites `impl-report.md`. Nothing was carried over from the first verification |
| `negative-cases-exercised` | pass | `## Negative and boundary cases exercised` below |
| `a-criterion-about-criteria-is-read` | pass | `## A criterion whose subject is other criteria`: AC16's eleven criteria named by ID, one verdict each read from their sentences, with the previously declared non-intersection shown closed and confirmed by mutation rather than by reading the new assertions |
| `adr-conformance-is-decided` | pass | `## ADR conformance`: five verdicts, each quoting a clause of `## Decision` with a file and line. `lint-documents --rule adr-conformance-is-decided --item WI-0001` → exit 0 |
| `invalidation-set-is-disposed` | pass | `## Invalidation set`: fourteen rows against fourteen entries, every one re-read against the new head. `lint-documents --rule invalidation-set-is-disposed --item WI-0001` → exit 0 |
| `tests-would-fail-without-the-change` | **pass** | `## Test sensitivity check`: fourteen mutations, fourteen red suites. The two that survived the first verification now fail |

## Negative and boundary cases exercised

Every one was *run* against `2f025c5`, with stdout, stderr and the exit code captured separately.

- **AC5** — income to an envelope that does not exist; the following listing proves nothing was created.
- **AC6** — `list` against a store path that does not exist: a line, exit 0, and no file created.
- **AC7** — a name already taken, with 400.00 in the envelope first, so the check is that the money survived the refusal.
- **AC8** — `12.567`, one digit over; `12.5`, one under; and `12.57`, the cent digit that is not a round ten and that no test exercised before this round.
- **AC10** — `0`, the boundary itself, and `-40`.
- **AC11 / AC7 together** — `new GROCERIES` against an existing `groceries`: the refusal fires through the folded match.
- **AC13** — the empty name, a leading space, and a trailing space. Both edges.
- **AC14** — no subcommand at all, and an unknown subcommand; store file confirmed absent afterwards.
- **AC15** — all five invocations, missing *and* extra arguments, across all three subcommands, with the listing checked afterwards. The three that failed the first verification were re-run specifically.
- **AC17** — `£12.50`, `1,200`, `12.5x`, `abc`.
- **Store damage** (ADR-0002) — `not json` and `{"format": 99, …}`. Both refused on read, and **both files `cat`-ed afterwards and found byte-identical**: the run that could not read the file did not overwrite it.
- **Path resolution** (ADR-0003) — `ENVEL_FILE` set *alongside* `XDG_DATA_HOME`, to test precedence rather than presence.
- **Both entry points on a failing path** — `bin/envel list extra` against `python3 -m envel list extra`, because this round changed the failure path and the success path alone would not have shown a divergence.

## Test sensitivity check

Fourteen behaviours were disabled one at a time on the branch head, the full suite run against
each, and the source restored with `git checkout -- .` after every one. The working tree was
confirmed clean afterwards.

| mutation | criteria it should break | suite | tests that failed |
|----------|--------------------------|-------|-------------------|
| `fold()` made case-sensitive | AC3, AC7, AC11, AC12 | fails | 5 |
| `create`'s duplicate check removed | AC7 | fails | 5 |
| `add_income`'s zero/negative check removed | AC10 | fails | 3 |
| `add_income`'s missing-envelope check removed | AC5 | fails | 2 |
| `create`'s name validation removed | AC13 | fails | 2 |
| two-decimal-place check removed | AC8 | fails | 3 |
| amount regex made permissive | AC17 | fails | 10 |
| empty listing prints nothing | AC6 | fails | 3 |
| refusals to stdout with exit 0 | AC16 | fails | 6 |
| the store is never saved | AC2, AC4, AC9 | fails | 14 |
| **the AC15 fix reverted to `parse_args`** | **AC15** | **fails** | **1 — `test_the_wrong_number_of_arguments`** |
| **`format_amount` rounds the last cent digit away** | **AC8, AC9** | **fails** | **2 — `test_an_amount_whose_cents_are_not_a_round_ten_is_exact`, `test_exactly_two_decimal_places`** |
| AC14 routed through a subcommand parser | AC14 | fails | 16 |
| the listing ordered by raw name, not folded | AC3 | fails | 1 — `test_one_line_per_envelope_ordered_by_folded_name` |

The two bolded rows are the ones that mattered. The first is the defect this round fixed, and it
now fails **exactly one** test — a precise, single-criterion signal, which is what it means for
AC15 to have its own covering case rather than sharing AC16's. The second is the insensitivity the
first verification found; it is closed.

The last row was added this round as a control: the first verification only ever mutated `fold()`
wholesale, which breaks four criteria at once, so AC3's ordering clause had never been isolated.
It is, and it is defended.

## Defects found

None. No criterion of this item failed, and no behaviour delivered by another item was found
wrong — there is no other item delivered yet. No bug was filed.

Two observations that are not defects and are carried forward rather than acted on:

1. **AC16's list of IDs is narrower than AC16's own first sentence**, omitting AC17. The universal
   sentence holds anyway, checked directly. This is a wording observation about a criterion, and
   editing a criterion is not this skill's to do.
2. **Two names differing only in internal whitespace are two envelopes.** `refine` left this
   deliberately unconstrained and recorded that it did. The tool's current answer is recorded here
   so that whoever meets it can see it was observed, not decided.

## Not verified, and why

- **The default store location was not exercised by writing to it.** ADR-0003's third branch is
  `~/.local/share/envel/envelopes.json`, and writing there would put a file in the real home
  directory of whoever runs this. I verified the *resolution* — `store_path()` returns exactly
  that path with neither environment variable set — and the directory-creation behaviour through
  the `XDG_DATA_HOME` branch, which is the same `mkdir(parents=True)` at `envel/store.py:75`. What
  is unchecked is that `~/.local/share` is writable, which is a fact about the machine.
- **Atomicity was not demonstrated by interrupting a write.** The mechanism is confirmed —
  `envel/store.py:77-80` writes a temporary beside the target and moves it with `os.replace` — and
  the round trip works, but killing a process mid-`os.replace` is not something this environment
  can stage. `os.replace` is atomic within a filesystem by contract, not by anything measured
  here. No acceptance criterion names atomicity; it comes from ADR-0002, and that is the extent of
  the claim.
- **The exact wording of every message is unverified on purpose.** `refine` left it open and the
  criteria constrain only what a message contains. This includes argparse's own sentences: the
  AC15 test asserts the usage line names the subcommand and is not the tool's, and quotes none of
  argparse's prose, so a Python upgrade that rewords `unrecognized arguments` will not break it.
  What is *not* left open, and is now asserted, is which of the two usage messages appears.
- **Two names differing only in internal whitespace** were not exercised; no criterion decides it.
  See `## Defects found`.
- **Concurrency was not tested.** Two processes writing the store at once has no criterion and no
  ADR; the tool is for one person at one terminal.
- **The first verification's report is not reproduced here.** It is a statement about `26d25ce`,
  which is no longer the branch head, and it is in git history rather than in this file.
