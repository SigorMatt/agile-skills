# Verification report — WI-0005

Verified-commit: 1695487b4a9962308019729f446b21ae2f216e11

Every verdict below rests on a command this execution ran against that commit, in a scratch store
addressed by `ENVEL_FILE` [src: ADR-0003], with the output quoted. The implementation report was
read **after** the criteria and after the evidence was gathered, and it is cited nowhere as
evidence for a criterion.

## Verdict

**Pass.** All twenty acceptance criteria are met. No criterion failed, none was ambiguous, none
was substituted, and no defect was found — neither this item's nor another's. The item goes to
`in-review`.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | `envel fix 999 --amount 14.00`; `envel list` captured before and after; `envel fix abc --amount 14.00`; `envel fix 5 --amount 14.00` with no envelope named; `envel remove 4` then `envel spend groceries 3.00` | `there is no entry '999'. Nothing has been changed.` exit 1, stdout empty; the listing before and after is byte-identical (`diff` silent) and the store's md5 is unchanged (`e1d570b4…`). `abc` takes the same path. `envel fix 5 --amount 14.00` → `corrected entry 5 in eating out, which now holds 66.00`, exit 0 — a bare number carrying no envelope reached an entry in a *different* envelope from the one entry `4` sits in. After removing `4`: `refs [1, 2, 3, 5, 6, 7] next-ref 8`, and the next spend recorded took `8` | The reference is one number counted once across everything: `envel entries` printed refs 1–7 over three envelopes, all distinct. Nothing renumbered on a removal and `4` was not reissued. The boundary case — removing the **highest**-numbered entry — is under the invalidation set below, where `next-ref` stayed at `4` and the next entry took `4` |
| AC2 | pass | `envel fix 4 --amount 14.00` on a 12.50 spend; then `--amount 9`; `--amount 14.005`; `--amount '£14.00'` | `corrected entry 4 in groceries, which now holds 196.00`, exit 0. groceries went 197.50 → 196.00, i.e. 12.50 back and 14.00 out. `--amount 9` printed `-9.00` on the entry's line — two decimals, no symbol. `14.005` → `'14.005' has more than two decimal places…` exit 1; `£14.00` → `…is not an amount: write a plain number…` exit 1 | The delivered money rules are inherited, not restated [src: WI-0001 AC8] |
| AC3 | pass | `envel fix 4 --on 2026-08-30`; `--on 7/9`; `--on 2026-9-6`; `--on 2026-09-12` (tomorrow); `--on 2026-09-11` (today) | `2026-08-30` → exit 0 and the entry moved into August's listing. `7/9` and `2026-9-6` → `'…' is not a date: write it as YYYY-MM-DD, such as 2026-09-07`, exit 1. `2026-09-12` → `2026-09-12 is in the future. Nothing has been changed.`, exit 1. Today → exit 0 | The store's md5 was identical after each refusal. The delivered `envel spend` was run beside it and gives the same two messages, differing only in `Nothing has been recorded.` [src: WI-0002 AC11], [src: WI-0002 AC12] |
| AC4 | pass | `envel fix 4 --description "lunch"`, then `--description ""`, then the same pair on a spend that had none; the JSON read back with `'description' in entry` | After `"lunch"`: `{…'ref': 4, 'description': 'lunch'}`. After `""`: `{'kind': 'spend', 'envelope': 'groceries', 'cents': -1250, 'on': '2026-09-06', 'at': '…', 'ref': 4}` and `description key present: False` | The key is **absent**, not empty — asserted against the stored document, not against the printed line. A blank `"   "` removes it too, which is plan step 3's rule and is a superset of AC4's `""` |
| AC5 | pass | `envel fix 4 --envelope "eating out"`; `--envelope nosuch`; `--envelope "EATING OUT"`; `envel list` each time | `corrected entry 4, moving it from groceries, which now holds 210.00, to eating out, which now holds 47.50`, exit 0. The listing went `eating out 60.00 → 47.50` (down by the 12.50 spend), `groceries 197.50 → 210.00` (up by it), `bills 90.00` unchanged. `nosuch` → `there is no envelope called 'nosuch'. Nothing has been changed.`, exit 1, md5 unchanged. `EATING OUT` matched and the entry stored `'envelope': 'eating out'` | The third envelope is the *no other envelope changed* check. Capitalisation matches and the stored spelling is the envelope's own [src: WI-0001 AC11], [src: WI-0002 AC3] |
| AC6 | pass | `envel fix 4 --amount 14.00 --on 2026-09-06 --description "lunch" --envelope "eating out"`; `envel fix 4` with no option; `envel fix 4 extra --amount 1.00` | All four applied in one pass: `{'kind': 'spend', 'envelope': 'eating out', 'cents': -1400, 'on': '2026-09-06', …, 'description': 'lunch'}`, exit 0. With no option: stdout empty, stderr `usage: envel fix [-h] [--amount AMOUNT] …` followed by `envel fix: error: give at least one of --amount, --on, --description or --envelope`, exit 2, store md5 unchanged | Two options at a time also work (`--amount 3.00 --description "bus"`). The usage is the **subcommand's**, as AC6 asks [src: WI-0001 AC15] |
| AC7 | pass | `envel list` captured before and after `envel fix 4 --amount 20.00`; separately, a second store built from scratch in which 20.00 was recorded at `envel spend` time, and the two listings diffed | Before: `bills 90.00 / eating out 60.00 / groceries 197.50`. After: only the `groceries` line differs, `197.50 → 190.00`. The as-if-recorded store prints `bills 90.00 / eating out 60.00 / groceries 190.00` and `diff` against the corrected store is **silent** | *"as though the corrected values had been recorded when the entry was first made"* is checked against an actual store in which they were, rather than by reasoning about the arithmetic |
| AC8 | pass | `envel summary 2026-09` and `2026-08` before and after `envel fix 4 --amount 20.00`, then after `envel fix 4 --on 2026-08-15` | Sept before: `groceries in 0.00 spent 12.50 moved 10.00 left 197.50`; after the amount fix: `spent 20.00 … left 190.00`. After the date fix, Sept: `groceries … spent 0.00 moved 10.00 left 190.00`; Aug: `groceries … spent 20.00 … left 180.00` | Setup note: the envelopes' `created` stamps were edited in the store file to 2026-07 so that an August summary has rows at all — `envel new` stamps today and a summary gives a row only to an envelope that existed by the end of the month [src: WI-0003 AC7]. The file is *"readable and repairable in any text editor"* [src: ADR-0002] and this is the same seeding `tests/test_cli.py::Entries` uses. The spend lands in **exactly one** month: 20.00 in August, 0.00 in September |
| AC9 | pass | `envel fix 4 --amount 300.00` where groceries holds 197.50 and entry 4 is a 12.50 spend from it; then `--amount 210.00` and `--amount 210.01` | `groceries holds 197.50, and this change would leave it 90.00 short. Nothing has been changed.`, exit 1, stdout empty, store md5 identical to the baseline. `210.00` (exactly to zero) → `corrected entry 4 in groceries, which now holds 0.00`, exit 0. `210.01` → `…would leave it 0.01 short.`, exit 1 | The message carries all three things AC9 names. The rule is checked **at** the boundary, one cent either side, not from a comfortable case. The listing never printed a negative figure in any run |
| AC10 | pass | `envel fix 4 --amount 0`; `envel fix 4 --amount=-5.00`; both again on an income reference | `an amount has to be more than zero, and 0.00 is not. Nothing has been changed.` and `…and -5.00 is not…`, exit 1 each, md5 unchanged | The delivered `envel spend 0` and `envel add 0` were run beside them and refuse in the same words [src: WI-0002 AC6] |
| AC11 | pass | `envel remove 4` with `stdin` redirected from `/dev/null`, then again with **fd 0 closed**; `envel remove 4 --yes` | `removed entry 4, 12.50 from groceries on 2026-09-06. groceries now holds 210.00`, exit 0, stderr empty, in both cases | The envelope, the date and the amount removed, and what the envelope holds afterwards. With no stdin at all the command still completed, so nothing prompts. `--yes` is `unrecognized arguments: --yes` — the flag does not exist to be given [src: WI-0005/Q-003] |
| AC12 | pass | `envel remove 999`; `envel remove abc`; `envel remove ""` | `there is no entry '999'. Nothing has been removed.`, exit 1, stdout empty, md5 unchanged; the same for `abc` and for the empty string | — |
| AC13 | pass | `envel fix 6 --amount 5.00`, `envel remove 6`, `envel fix 7 --amount 5.00`, `envel remove 7` — refs 6 and 7 being the two halves of one move | `entry 6 is a move between envelopes, and a move cannot be corrected. Nothing has been changed.` / `…cannot be removed. Nothing has been removed.`, and the same for 7; exit 1 each; the store md5 equals the baseline after all four | **Both** halves refused by **both** commands. The code refuses on `entry["kind"]` alone [src: envel/envelopes.py:351], [src: envel/envelopes.py:442] — it never looks for the partner, which is what keeps `ADR-0007`'s *nothing links them* true |
| AC14 | pass | `envel fix 4 --amount 33.00 --on 2026-08-03`, then `envel list`, `envel summary 2026-08` and `envel entries --month 2026-08` as three further processes; then `envel remove 5` and two more | After the fix, a separate `envel list` printed `groceries 177.00`, a separate summary printed `groceries … spent 33.00 … left 167.00`, a separate listing printed `4  2026-08-03  spend  groceries  -33.00  shop`. After the removal, a separate listing no longer carried ref 5 and `eating out` read `80.00` | Every invocation in this whole report is its own process; this row is the case made deliberately, with the reader commands run after the writer exited |
| AC15 | pass | 24 invocations, each capturing stdout, stderr and the exit code separately — see `## A criterion whose subject is other criteria` below for the table | Refusals: exit non-zero, `stdout=0` bytes, `stderr>0` on every one of the eleven criteria AC15 names. Successes: exit 0, `stderr=0` bytes, `stdout>0` on every one of the eight | Checked **case by case** against the criteria AC15 names, not by asserting the convention once [src: WI-0002 AC13], [src: docs/architecture/overview.md] |
| AC16 | pass | On income ref 1: `--amount 180.00`; `--envelope BILLS`; `--envelope nosuch`; `--on 2026-09-01`; `--description x`; `--description ""`. On an income in an envelope with no spends: `--envelope groceries` | `--amount 180.00` → `corrected entry 1 in groceries, which now holds 177.50`, exit 0, and the stored entry is `{'kind': 'income', 'envelope': 'groceries', 'cents': 18000, 'at': …, 'ref': 1}` — no `on`, no `description` gained. `--envelope groceries` on the spend-free income → `corrected entry 8, moving it from savings, which now holds 0.00, to groceries, which now holds 247.50`, exit 0. `--on` and `--description` (including `""`) → `entry 1 is income, which carries no date and no description. Nothing has been changed.`, exit 1, md5 unchanged each time. `--envelope nosuch` → AC5's refusal. `--amount 0` on an income → AC10's refusal | Exactly two options reach an income and exactly two are refused on it [src: WI-0005/Q-006]. `--envelope BILLS` refused for a different reason — AC18's shortfall — which is that rule and not a gap here |
| AC17 | pass | `envel remove 8` on an income, fd 0 closed; `envel remove 8 --income` | `removed entry 8, 50.00 from savings. savings now holds 0.00`, exit 0, stdout 60 bytes, stderr 0 | The envelope and the amount and what it holds afterwards, and **no date** — the same subcommand as AC11 with no flag and none accepted (`unrecognized arguments: --income`) [src: WI-0005/Q-007] |
| AC18 | pass | A store where `holiday` holds 100.00 of income (ref 1) with 90.00 spent from it (ref 2), so it holds 10.00. Then all three routes: `envel remove 1`; `envel fix 1 --amount 50.00`; `envel fix 1 --envelope spare`. Then the boundary: `--amount 90.00` and `--amount 89.99` | `holiday holds 10.00, and removing this would leave it 90.00 short. Nothing has been removed.` / `…and this change would leave it 40.00 short. Nothing has been changed.` / `…would leave it 90.00 short. Nothing has been changed.` — exit 1 each, and the store JSON is **deep-equal** to the baseline after all three. `--amount 90.00` → exit 0, `holiday now holds 0.00`; `--amount 89.99` → `…would leave it 0.01 short.`, exit 1 | All **three** routes AC18 names, including the change-of-envelope route that takes an income's whole amount out without any figure being reduced. Checked at the boundary, one cent either side |
| AC19 | pass | Eleven invocations, each pairing an option that would be accepted with one that is refused, each preceded and followed by a snapshot of `envel list` + `envel entries` for three months, compared by digest — plus the AC19 case written out in full, with the entry's own line grepped from `envel entries --month 2026-07` | Every one of the eleven: `UNCHANGED`. The written-out case: `envel fix 1 --amount 20.00 --on 2026-09-01` → `entry 1 is income, which carries no date and no description. Nothing has been changed.`, exit 1; `diff` of the three-line July listing before and after is silent, and so is `diff` of the whole `envel list` | The eleven cover the refusals AC19 names at AC1, AC3, AC5, AC6, AC9, AC10, AC13, AC16 and AC18, each reached while another option was given. Non-vacuous: the compared listing carried three entry lines, not zero |
| AC20 | pass | `envel entries --month …` captured around each of `--amount 14.00`, `--on 2026-08-15`, `--envelope "eating out"` and `remove 4`; ref 4's presence counted in every month; `envel entries groceries --month …` parsed and reconciled after each of the four | `--amount`: `4  2026-09-06  spend  groceries  -12.50  shop` → `4  2026-09-06  spend  groceries  -14.00  shop`, rest of the line identical. `--on`: absent from September, present **once** in August (`2026-07: 0, 2026-08: 1, 2026-09: 0`). `--envelope`: `4  2026-09-06  spend  eating out  -12.50  shop`. `remove`: `2026-07: 0, 2026-08: 0, 2026-09: 0`. Reconciliation, e.g. after the amount fix — `opening 200.00 + lines -4.00 = 196.00 ; closing 196.00 → RECONCILES`, and likewise in every month that had lines | The *once* in AC20 is a count across **every** month, not an assertion about the new one [src: WI-0006 AC2], [src: WI-0006 AC7], [src: WI-0006 AC9] |

## A criterion whose subject is other criteria

Two criteria here have criteria as their subject, and both were **read** against the new
behaviour and then evidenced, rather than answered with a green suite.

### AC15 — the stream, the exit code, and the criteria it names

AC15 names nineteen obligations by ID. Each was reached as its own invocation, with stdout and
stderr captured to separate files and measured in bytes.

| the criterion AC15 names | shape | invocation | exit | stdout | stderr | verdict |
|---|---|---|---|---|---|---|
| AC1 | refusal | `envel fix 999 --amount 1.00` | 1 | 0 B | 51 B | still true |
| AC3 | refusal | `envel fix 4 --on 2026-12-01` | 1 | 0 B | 55 B | still true |
| AC3 | refusal | `envel fix 4 --on 7/9` | 1 | 0 B | 64 B | still true |
| AC5 | refusal | `envel fix 4 --envelope nosuch` | 1 | 0 B | 64 B | still true |
| AC6 | refusal | `envel fix 4` | 2 | 0 B | 229 B | still true |
| AC9 | refusal | `envel fix 4 --amount 300.00` | 1 | 0 B | 94 B | still true |
| AC10 | refusal | `envel fix 4 --amount 0` | 1 | 0 B | 79 B | still true |
| AC10 | refusal | `envel fix 4 --amount=-5.00` | 1 | 0 B | 80 B | still true |
| AC12 | refusal | `envel remove 999` | 1 | 0 B | 51 B | still true |
| AC13 | refusal | `envel fix 6 --amount 5.00` | 1 | 0 B | 95 B | still true |
| AC13 | refusal | `envel remove 6` | 1 | 0 B | 93 B | still true |
| AC16 | refusal | `envel fix 1 --on 2026-09-01` | 1 | 0 B | 87 B | still true |
| AC16 | refusal | `envel fix 1 --description x` | 1 | 0 B | 87 B | still true |
| AC18 | refusal | `envel fix 1 --envelope bills` | 1 | 0 B | 93 B | still true |
| AC19 | refusal | `envel fix 1 --amount 20.00 --on 2026-09-01` | 1 | 0 B | 87 B | still true |
| AC2 | success | `envel fix 4 --amount 14.00` | 0 | 55 B | 0 B | still true |
| AC4 | success | `envel fix 4 --description lunch` | 0 | 55 B | 0 B | still true |
| AC4 | success | `envel fix 4 --description ""` | 0 | 55 B | 0 B | still true |
| AC5 | success | `envel fix 4 --envelope "eating out"` | 0 | 106 B | 0 B | still true |
| AC7 | success | `envel fix 4 --amount 20.00` | 0 | 55 B | 0 B | still true |
| AC11 | success | `envel remove 4` | 0 | 80 B | 0 B | still true |
| AC16 | success | `envel fix 1 --amount 180.00` | 0 | 55 B | 0 B | still true |
| AC16 | success | `envel fix 8 --envelope groceries` | 0 | 102 B | 0 B | still true |
| AC17 | success | `envel remove 8` (an income) | 0 | 60 B | 0 B | still true |
| AC20 | success | `envel entries --month 2026-09` | 0 | 168 B | 0 B | still true |

AC6's exit code is `2` rather than `1` because the refusal is `argparse`'s own, which is the
delivered convention for a command line of the wrong shape [src: WI-0001 AC15] and is what AC6
asks for by name. AC15 says *non-zero*, and `2` is non-zero.

**Non-intersection: none for AC15.** The `succeeded()` and `refused()` helpers in
`tests/test_cli.py::Corrections` assert the stream, the emptiness of the other stream and the exit
code on every case in the class, so every criterion AC15 names is exercised together with AC15's
own rule by something executable. The table above is this execution's independent reading of the
same nineteen obligations, not a citation of those helpers.

### AC19 — a refused invocation applies none of itself

AC19 names nine criteria whose refusals must leave nothing applied. Each was reached with a
second, acceptable option in the same invocation.

| the criterion AC19 names | invocation | exit | listing + three months' entries |
|---|---|---|---|
| AC16 | `envel fix 1 --amount 20.00 --on 2026-09-01` | 1 | unchanged |
| AC1 | `envel fix 999 --amount 20.00 --description x` | 1 | unchanged |
| AC3 | `envel fix 4 --description ok --on 2026-12-01` | 1 | unchanged |
| AC5 | `envel fix 4 --amount 5.00 --envelope nosuch` | 1 | unchanged |
| AC5 | `envel fix 4 --amount 5.00 --description later --on 2026-09-02 --envelope nosuch` | 1 | unchanged |
| AC9 | `envel fix 4 --amount 300.00 --description overspend` | 1 | unchanged |
| AC10 | `envel fix 4 --amount 0 --description zero` | 1 | unchanged |
| AC13 | `envel fix 6 --amount 5.00 --description movefix` | 1 | unchanged |
| AC16 | `envel fix 1 --amount 20.00 --description payslip` | 1 | unchanged |
| AC18 | `envel fix 1 --envelope bills --amount 20.00` | 1 | unchanged |
| AC6 | `envel fix 4` | 2 | unchanged |

**Non-intersection, stated in those words: nothing executable exercises AC19 together with the
refusals of AC1, AC6, AC9, AC10, AC13 or AC18.** The suite's AC19 cases are
`tests/test_corrections.py::UnchangedOnRefusal`'s three — which pair an accepted option with
AC16's, AC5's and AC3's refusals — and `tests/test_cli.py::Corrections::test_a_refused_invocation_applies_none_of_its_accepted_options`,
which is AC16's again. Six of the nine combinations have no standing case.

**Waived by name, for AC1, AC6, AC9, AC10, AC13 and AC18.** The reason is structural rather than
budgetary. AC19 is not nine behaviours; it is one, and it lives in two lines that no refusal can
route around: `correct` takes its `copy.deepcopy` **after** all six of its early refusals
[src: envel/envelopes.py:378], and the seventh — the balance refusal — reads `candidate` and
returns without handing a document back [src: envel/envelopes.py:396], while `envel/cli.py` saves
only what an `Ok` carries [src: envel/cli.py:217]. The three `UnchangedOnRefusal` cases pin that
mechanism at the function level, where a mutation of the caller's store is visible by deep
equality; the mutation run below confirms they bite, and a further mutation replacing the
deep-copy with the live store failed five tests. A sixth, seventh and eighth CLI round-trip would
re-exercise the same two lines through a slower path. The six combinations are verified here by
hand, and that is what this row is.

## ADR conformance

One verdict per ID in the plan's `## Binding ADRs` list, each quoting the clause of that ADR's
`## Decision` the change is judged against.

| ADR | verdict | clause quoted from its Decision | file and line, or why not engaged |
|-----|---------|--------------------------------|-----------------------------------|
| `ADR-0001` | conforms | *"Two functions in `envel/money.py` are the only places the two forms meet: one parses the text the user typed into cents, one renders cents back into text. No other module converts between them, and no amount is ever held as a `float`"* | Every amount this change prints goes through `money.format_amount` — ten call sites, at `envel/envelopes.py:368`, `:402`, `:403`, `:409`, `:417`, `:419`, `:459`, `:460`, `:467`, `:474` — and the one parse is `money.parse_amount(arguments.amount)` at `envel/cli.py:183`. Enumerated over the branch's added lines: `grep -E '^\+' | grep -E 'float\(|/ *100|% *100|\.2f'` → **no matches**, so no conversion was added outside `envel/money.py` |
| `ADR-0002` | conforms | *"`entries` is ordered as written, and an envelope's balance is the sum of `cents` over the entries naming it — the second half with no branch on `kind`"* (the clause as it now reads at v4) | `balance` is untouched at `envel/envelopes.py:63` and has no `kind` branch. Order: correcting the **first** entry of a three-entry store left `[1, 2, 4]` in that order, and `remove` is a filter that preserves order [src: envel/envelopes.py:451]. The clause this change **falsified** — *"append-only within a run"* — was repaired as an erratum at v4, which is the `to-update` row below |
| `ADR-0003` | conforms | *"The store path is, in order: `$ENVEL_FILE` … Missing parent directories are created when the store is first written"* — one function in `envel/store.py` resolves it | The one resolver is `envel/store.py:24`, untouched by this change. Neither new operation sees a path: `grep -n 'store_path\|ENVEL_FILE\|envelopes\.json' envel/envelopes.py envel/summary.py envel/money.py envel/dates.py` → **no matches**. `envel/store.py` is not in `git diff --stat main..HEAD`. Every criterion above was observed through `ENVEL_FILE` |
| `ADR-0004` | conforms | *"there are two ways to start it, both reaching the same `main`"* | The two new subcommands are registered in the one parser `main` builds, at `envel/cli.py:126`, and `main` is what both entry points call — `envel/__main__.py:5` and `bin/envel:9`. Both reach them, run here: `python3 -m envel fix 2 --amount 3.00` → exit 0, and `./bin/envel fix 2 --amount 4.00` → exit 0, `./bin/envel remove 2` → exit 0. Neither entry point is in the diff |
| `ADR-0005` | conforms | *"`commands.test`: `python3 -m unittest discover -s tests -t .` … `commands.lint`: `python3 -m compileall -q envel tests`"*, standard library only | The new code imports nothing outside the standard library: `envel/envelopes.py:8` is `import copy` and its intra-package import at `envel/envelopes.py:12` is `from . import dates, money`. Both commands run by this execution against the branch head: `Ran 299 tests … OK`, exit 0; `compileall` exit 0. Every import in `envel/` enumerated (`grep -nE '^import \|^from '` → 15 lines) and all fifteen are stdlib or intra-package |
| `ADR-0006` | conforms | *"`on` is present on every spend entry … It is never absent and never null"*, and *"`description` is present only when one was typed. Absent means there was none"* | `correct` only ever **sets** `on` [src: envel/envelopes.py:386] and nothing in the tool deletes one. Boundary checked: `envel fix 2 --on ""` is refused by `dates.parse_date` (`'' is not a date…`, exit 1), and after a correction giving all of `--amount`, `--description ""` and `--envelope` the entry reads `'on' present: True, non-null: True, 'description' present: False`. The removal is by `pop` [src: envel/envelopes.py:389], so the key is absent, not empty |
| `ADR-0007` | conforms | *"No field links the two entries to each other"*, and the two-entry shape with `cents` carrying the direction | Both AC13 refusals read `entry["kind"]` on the single entry they were handed — `envel/envelopes.py:351` and `:442` — and neither looks for a partner. Enumerated: `grep -n '"move"' envel/*.py` → 11 lines, of which this change adds exactly those two; the other nine are `move`'s own appends and the summary's reading, all unchanged. Both halves were refused independently, by both commands |
| `ADR-0008` | conforms | *"A month is the seven-character string `YYYY-MM`, and it is compared as a string"*, and *"Every figure is a filtered sum over the entries naming the envelope"* | The month rule is `entry_month` at `envel/summary.py:42`, byte-identical to `main`. Not one line of month logic was added: `envel/summary.py` and `envel/dates.py` are byte-identical to `main` (`git diff --stat` lists neither), and neither `correct` nor `remove` mentions a month. AC8's *exactly one month* was produced by changing `on` alone and observed in the two summaries |
| `ADR-0009` | conforms | *"`envel/summary.py` holds this project's reports … `summary` imports `envelopes`; `envelopes` does not import `summary`"* | Both operations are in `envel/envelopes.py`. Its imports are `copy`, `dataclasses`, `datetime` and `from . import dates, money` [src: envel/envelopes.py:8], with **no `summary`** — the temptation the plan's risk list named (reusing `entry_date` for the removal line) was not taken; `remove` reads `entry["on"]` directly, guarded by `if "on" in entry` [src: envel/envelopes.py:468] |
| `ADR-0010` | conforms | *"An entry carries `ref`, a positive integer, written when the entry is appended and never changed afterwards"*, and *"The counter is the only source of a new reference. Nothing derives one from a position, a length or a maximum"* | Enumerated every write of `ref`/`next-ref` in `envel/`: `envelopes.py:50` (the counter advancing inside `take_ref`), `:111`, `:173`, `:270`, `:276` (the four appends, each via `take_ref`), and `store.py:36`, `:53`, `:55` (the format-1 upgrade). All eight predate this branch. Every line this change adds that touches `ref` — `:309`, `:354`, `:359`, `:409`, `:415`, `:445`, `:451`, `:474` — **reads or compares** it; `:451` is `remove`'s filter. Boundary falsifier below |
| `ADR-0011` | conforms | *"A correction **mutates the entry** identified by `ref`, in the `entries` list, leaving its position in the list and its `ref` untouched. A removal **deletes that entry** from the list. Nothing is appended by either"*, and *"The invariant is checked against the candidate document, not the live one"* | Position preserved (`[1, 2, 4]` before and after correcting the first entry); `ref` preserved (entry 4 stayed 4 through a four-option correction); nothing appended (the entry count falls by one on a removal and is constant on a correction). `next-ref` untouched by a removal. The invariant reads `candidate` [src: envel/envelopes.py:396], [src: envel/envelopes.py:453], which is why AC9's message can quote the *original* balance and the shortfall together |

**No ADR outside the plan's list was found engaged.** `ADR-0012` is a methodology ADR about the
orchestrator's halt count and has no subject in this change.

## Invalidation set

One row per entry in the plan's set. Every entry disposed `verified-still-true` was **reopened**
and read against the branch head; where the sentence is quantified, the row carries the
enumeration, the members, and the falsifier that was looked for.

| document | disposition | what I reopened, and what I found |
|----------|-------------|-----------------------------------|
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` `## Decision`, the `entries` bullet | to-update | **Done, and checked.** The document is at `version: 4`, `updated-for: WI-0005`, with a `## Change log` row and a `## Corrections` row of kind `erratum`. The new text is true of the code: the list is ordered as written (position preserved through a correction, `remove` is an order-preserving filter) and `balance` still sums `cents` with no `kind` branch [src: envel/envelopes.py:63]. The clause that was false — *"append-only within a run"* — is gone and the **decision** is untouched |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` `## Consequences` + Reversibility | verified-still-true | Reopened. *"readable and repairable in any text editor"* — demonstrated directly: this execution edited the store's `created` stamps by hand for AC8 and the tool read the file back without complaint. The reversibility sentence is about changing the document's **shape**; no key was added, removed or renamed — the stored document's keys are `['entries', 'envelopes', 'format', 'next-ref']` and an entry's are `['at', 'cents', 'envelope', 'kind', 'on', 'ref']`, `FORMAT` is still `2`, and `envel/store.py` is byte-identical to `main` |
| `docs/architecture/adr/ADR-0010-an-entry-carries-its-own-reference.md` `## Consequences`, *"A reference survives a removal"* | verified-still-true | Reopened. True, and now observed rather than predicted: after `envel remove 4`, `refs [1, 2, 3, 5, 6, 7]` — 5, 6 and 7 kept their own numbers, none was shifted down into the hole |
| `docs/architecture/adr/ADR-0010-an-entry-carries-its-own-reference.md` `## Decision` 5, *"The counter is the only source of a new reference"* | verified-still-true | Reopened. **Set:** every line in `envel/` mentioning `ref`, `next-ref` or `take_ref`, enumerated with `grep -n 'ref"\]\|"ref":\|next-ref\|take_ref' envel/*.py` → 21 lines in three files. **Members and verdicts:** the eight writes are `envelopes.py:50` and the four `take_ref(store)` appends, plus `store.py:36`, `:53`, `:55` — all unchanged by this branch. The eight lines this change adds all read or compare. **Falsifier looked for, at the boundary:** removing the **highest**-numbered entry and then recording a new one — the case where deriving a reference from a maximum or a length would be invisible in every other test. A store with refs `[1, 2, 3]` and `next-ref 4`: after `envel remove 3` → `refs [1, 2] next-ref 4`; the next spend took **4**, and `next-ref` went to 5. A derived counter would have reissued `3` |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` two-entry shape, *"nothing links them"* | verified-still-true | Reopened. **Set:** every mention of the move kind in `envel/`, `grep -n '"move"' envel/*.py` → 11 lines. **Members:** `envelopes.py:207` (docstring), `:269`, `:275` (the two appends), `summary.py:67`, `:129`, `cli.py:59`, `:127`, `:171` — eight unchanged; `envelopes.py:351`, `:442` added. **Verdict:** the two added lines read `entry["kind"]` on the entry handed in. **Falsifier:** a refusal that found the partner — e.g. one that named the *other* envelope in its message, or that refused ref 6 by inspecting ref 7. Both messages name only the entry given (`entry 6 is a move between envelopes…`), and refusing ref 7 produced the same message about 7 |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` `on` and `description` | verified-still-true | Reopened. **Set:** every write or delete of either key. `on` is written at `envelopes.py:171`, `:269`, `:275` and `:385` (`correct`, set only) and is **never** deleted anywhere in `envel/`; `description` is written at `:176` and `:391` and removed at `:389` by `pop`. **Falsifier, at the boundary:** a spend with no `on`, or one carrying an empty `description`. `envel fix 2 --on ""` → refused by `dates.parse_date`, exit 1; after a correction setting all four fields with `--description ""` the entry reads `'on' present: True, non-null: True, 'description' present: False` |
| `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` reporting vs operations | verified-still-true | Reopened. Both operations are in `envel/envelopes.py`; `envel/summary.py` is not in `git diff --stat main..HEAD`. `envelopes.py` imports `copy, dataclasses, datetime, dates, money` and not `summary` |
| `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md` month as string, filtered sums | verified-still-true | Reopened. No month logic was added — `summary.py` and `dates.py` are byte-identical to `main`, and neither new function mentions a month. AC8 crossing the boundary is `entry_month` applied to a changed `on`; the corrected spend appeared in **one** month and its old month read `spent 0.00` |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` money.py the only meeting point | verified-still-true | Reopened. **Set:** every conversion between text and cents added on this branch, enumerated over the diff's added lines → `money.format_amount` × 10 and `money.parse_amount` × 1. **Falsifier:** any `float(`, `/ 100`, `% 100` or `.2f` in the added lines → `grep` over the same window returns **no matches** |
| `docs/architecture/adr/ADR-0003-store-location.md` store path in one function | verified-still-true | Reopened. `grep -n 'store_path\|ENVEL_FILE\|envelopes\.json' envel/envelopes.py envel/summary.py envel/money.py envel/dates.py` → no matches; `envel/store.py` not in the diff |
| `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` two entry points, one `main` | verified-still-true | Reopened, by running both: `python3 -m envel fix …` exit 0 and `./bin/envel fix …` / `./bin/envel remove …` exit 0. The falsifier — a subcommand reachable from one entry point and not the other — was looked for by driving `fix` **and** `remove` through the shim as well as the module |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` the two commands, stdlib only | verified-still-true | Reopened by running both over everything the change touched: tests exit 0 (`Ran 299 tests`, `OK`), lint exit 0. Imports enumerated (15 lines): all stdlib or intra-package |
| `docs/architecture/overview.md` `## The parts`, the seven operations | verified-still-true | Reopened. `create`, `add_income`, `listing`, `record_spend`, `move`, `correct`, `remove` — all seven are `def`s in `envel/envelopes.py`, and neither new one landed elsewhere |
| `docs/architecture/overview.md` `## The parts`, dependency direction | verified-still-true | Reopened. **Set:** every import in `envel/`, `grep -nE '^import \|^from ' envel/*.py` → 15 lines. `cli.py:13` imports all five below it; `summary.py:28` imports `dates, envelopes, money`; `envelopes.py:12` imports `dates, money` and **not** `summary`; `store.py`, `money.py`, `dates.py` import nothing intra-package. **Falsifier:** an `envelopes → summary` edge. Absent |
| `docs/architecture/overview.md` `## The shape of it`, nothing below `cli` prints or exits | verified-still-true | Reopened. `grep -n 'print(\|sys\.exit' envel/envelopes.py envel/summary.py envel/store.py envel/money.py envel/dates.py` → **no matches** (exit 1). Both new operations return their line inside `Ok` and their message inside `Refusal` |
| `docs/architecture/overview.md` `## The shape of it`, *"only if something changed"* | verified-still-true | Reopened. **Falsifier:** a refusal that wrote. Every refusal in this report was measured by the store file's md5 or by deep equality of the parsed JSON, across all eleven AC19 combinations and every individual refusal above — not one wrote. `envel fix <ref>` with no option exits before the store is opened at all [src: envel/cli.py:144] |
| `docs/architecture/overview.md` `## The data`, the entries paragraph at v9 | verified-still-true | Reopened clause by clause: the list was append-only until this item (true — `remove` filters [src: envel/envelopes.py:451]); a correction edits in place (position preserved); entries are still ordered as written and summed with no `kind` branch; `format` stays `2` (`FORMAT = 2` at `envel/store.py:11`, file unchanged) |
| `docs/architecture/overview.md` `## The data`, `ref` *"never changed afterwards"* | verified-still-true | Reopened. Same enumeration as `ADR-0010`'s row. Observed directly: after `envel fix 4 --amount 14.00 --on 2026-09-06 --description "lunch" --envelope "eating out"` the stored entry still reads `'ref': 4`, `'kind': 'spend'` and its original `'at'` |
| `docs/architecture/overview.md` `## The data`, the move paragraph | verified-still-true | Reopened. Same enumeration as `ADR-0007`'s row; nothing added reads the adjacency |
| `docs/architecture/overview.md` `## Conventions`, stdout/exit 0, stderr/non-zero | verified-still-true | Reopened. **Set:** the paths this change adds — two successes and the refusals of AC1 (×2 commands), AC3, AC5, AC6, AC9, AC10, AC12, AC13 (×2), AC16 (×2), AC18. **Verdict:** the AC15 table above measured every one of them individually, in bytes. No path writes to both streams and none writes to the wrong one |
| `docs/architecture/overview.md` `## Conventions`, two decimals, no symbol | verified-still-true | Reopened. Same enumeration as `ADR-0001`'s row, and observed: `--amount 9` printed `-9.00`; `--amount 14.005` and `--amount '£14.00'` were refused rather than rounded or accepted |
| `docs/architecture/overview.md` `## Conventions`, dates parsed in `envel/dates.py` and nowhere else | verified-still-true | Reopened. `--on` is parsed by `dates.parse_date` at `envel/cli.py:186`, compared against `dates.today()` and written with `dates.format_date`. `envel/dates.py` is not in the diff and no date string is sliced or string-compared in the new code |
| `docs/architecture/overview.md` `## What is not decided yet`, *"Nothing. Every item of `EP-001` has had its design taken"* | verified-still-true | Reopened. **Set:** the items of `EP-001`, enumerated from `tracker/board.md` → `WI-0001`…`WI-0006`, six. **Verdict:** five `done`, this one at `verifying` with its plan and ADRs written. **Falsifier:** a bug item filed by this execution, which would add a seventh with no design. **This execution filed none** — see `## Defects found` — so the family the sentence quantifies over has not grown and the sentence is still true |
| `docs/architecture/overview.md` `## Engagement state` | owned-by-ending | Left exactly as it is. `git diff main..HEAD -- docs/architecture/overview.md` is **empty** on this branch, so this item edited no `## Engagement state` section [src: toolkit: doc-header.md engagement-state rules "Between then and the ending, **no execution writes one.**"] |
| `docs/product/vision.md` `## What it is for`, the correction paragraph | verified-still-true | Reopened against the delivered commands: a correction reaches all four fields of a spend (AC2–AC5, run), a spend is removed by a command that says what it took (AC11, run), a below-zero correction is refused with the shortfall named (AC9, run), moves stay outside it (AC13, run). Every clause matches what the tool does |
| `docs/product/vision.md` `## What it is for`, the income paragraph | verified-still-true | Reopened. The amount and the envelope and no date (AC16, run — `--on` and `--description` refused); removal by the same command with no flag (AC17, run — `--income` is `unrecognized`); the shortfall rule reaching a removal (AC18, run, all three routes) |
| `docs/product/vision.md` `## What it is for`, *"the number an entry is given stays that entry's"* | verified-still-true | Reopened. **Set:** the two events that can break it — a removal, and an entry recorded after one. **Falsifier at the boundary:** removing the highest-numbered entry, then recording. `refs [1,2,3] next-ref 4` → remove 3 → `refs [1,2] next-ref 4` → the next entry took **4**. The number written down last week still means what it meant |
| `docs/product/vision.md` `## What it deliberately is not`, no network | verified-still-true | Reopened. **Set:** every import added on this branch. `envel/envelopes.py` and `envel/cli.py` add none; the test modules add `copy`, `datetime`, `unittest`, `re`. **Falsifier:** any `socket`, `http`, `urllib`, `requests` — none present anywhere in `envel/`, per the 15-line import enumeration |
| `docs/product/vision.md` `## Engagement state` | owned-by-ending | Left exactly as it is. `docs/product/vision.md` is not in `git diff --stat main..HEAD` at all |

**This execution wrote no document under `docs/`.** `git status` was clean before and after; the
only file this skill changed outside `tracker/` is none.

## Gates

- `tests-pass` → **pass**. `python3 -m unittest discover -s tests -t .` → exit 0,
  `Ran 299 tests in 40.040s`, `OK`. Run by this execution on the branch head, not quoted from the
  implementation report.
- `lint-clean` → **pass**. `python3 -m compileall -q envel tests` → exit 0.
- `workspace-valid` → **pass**. `scripts/validate-workspace .` → exit 0, `0 errors, 0 warnings`,
  7 items and 13 documents checked.
- `every-criterion-independently-checked` → **pass**. The `## Criteria` table names, for each of
  AC1 to AC20, a command this execution ran and its actual output. Roughly 110 invocations of the
  tool against scratch stores under `ENVEL_FILE`.
- `negative-cases-exercised` → **pass**. Every refusal was *triggered*: see
  `## Negative and boundary cases exercised`. Fifteen refusal paths plus eleven AC19 combinations
  plus nine extra boundaries, each with its exit code and both streams measured.
- `a-criterion-about-criteria-is-read` → **pass**. AC15 and AC19 both have criteria as their
  subject; each names its covered criteria by ID, each has a per-criterion verdict read from the
  text, and the AC19 non-intersection is stated in those words and waived by name for six
  combinations with the reason.
- `adr-conformance-is-decided` → **pass**.
  `scripts/lint-documents --rule adr-conformance-is-decided --item WI-0005` → exit 0. Eleven
  verdicts, each quoting a clause of that ADR's `## Decision`.
- `invalidation-set-is-disposed` → **pass**.
  `scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0005` → exit 0. All 29
  rows carry a disposition; the 26 `verified-still-true` rows were reopened and read here; the one
  `to-update` row names a document that was updated with a version bump and a change-log row; the
  two `owned-by-ending` rows were left untouched and both documents are absent from the branch's
  diff.
- `tests-would-fail-without-the-change` → **pass** (advisory). See
  `## Test sensitivity check` — fourteen mutations, each reverted, every one caught.

## Negative and boundary cases exercised

Triggered, not read about. Each was run as its own process with both streams captured.

- **Identity.** `fix 999`, `fix abc`, `fix 0`, `fix 99999999999999999999`, `fix 4.0`,
  `remove 999`, `remove abc`, `remove ""` — all refused, exit 1, nothing written.
  `fix -- -1 --amount 1.00` is `argparse`'s `unrecognized arguments`, exit 2, nothing written.
- **An empty store.** `fix 1` and `remove 1` against a path with no file → both refused with
  `there is no entry '1'`, exit 1, and no file was created.
- **The below-zero boundary, both rules, one cent either side.** AC9: `--amount 210.00` → exit 0
  and `0.00`; `--amount 210.01` → refused, `0.01 short`. AC18: `--amount 90.00` → exit 0 and
  `0.00`; `--amount 89.99` → refused, `0.01 short`.
- **The future-date boundary.** `--on <today>` → exit 0; `--on <tomorrow>` → refused.
- **The empty and blank description.** `--description ""` and `--description "   "` both remove
  the key; asserted against the stored JSON with `'description' in entry` → `False`.
- **The empty envelope name and the empty date.** `--envelope ""` → `there is no envelope called
  ''`; `--on ""` → `'' is not a date`.
- **Every refusal reached with another option in the same invocation** — eleven combinations, all
  `UNCHANGED` (the AC19 table).
- **Both halves of a move, from both commands** — four refusals.
- **The highest-numbered entry removed, then a new entry recorded** — the `next-ref` falsifier.
- **No stdin at all.** `envel remove <ref>` with file descriptor 0 **closed** completed with
  exit 0, so no code path waits for a confirmation.

## Test sensitivity check

Fourteen mutations were applied one at a time to the branch head, the full suite run against each,
and the file restored from a pristine copy afterwards. The suite is green again at the end
(`Ran 299 tests … OK`) and `git status` is clean, so nothing was left behind.

| behaviour disabled | criteria it covers | result |
|---|---|---|
| `find_entry` falls back to the first entry | AC1, AC12 | FAILED (failures=6) |
| the future-date refusal removed | AC3 | FAILED (failures=3) |
| the unknown-envelope refusal removed | AC5 | FAILED (failures=1, errors=2) |
| the invariant check in `correct` removed | AC9, AC18 | FAILED (failures=7) |
| the invariant check in `remove` removed | AC18 | FAILED (failures=5) |
| the zero/negative amount refusal removed | AC10 | FAILED (failures=5) |
| the move refusal in `correct` removed | AC13 | FAILED (failures=5) |
| `correct` mutates the caller's store (no deep copy) | AC19 | FAILED (failures=5) |
| an empty description stored instead of the key deleted | AC4 | FAILED (failures=3) |
| the date put on every removal line | AC11, AC17 | FAILED (failures=2) |
| the *no option given* check removed | AC6 | FAILED (failures=1) |
| the sign of a corrected amount dropped | AC2 | FAILED (failures=11) |
| `next-ref` lowered on a removal | AC1 | FAILED (failures=1) |
| `--on` accepted on an income | AC16 | FAILED (failures=6) |

Every mutation was caught. No test passed against an absent implementation. AC7, AC8, AC14 and
AC20 have no mutation of their own because they have no code of their own — they fall out of
`ADR-0011`, and the mutations above that change what is *stored* (the sign, the description key,
the date, the counter) are what their tests read.

## Defects found

**None.** No criterion of this item failed, so there is no send-back. No behaviour delivered by
another item failed against that item's own criteria, so no bug was filed.

**One finding in the record, which is neither a send-back nor a bug, and which `review-close`
should decide on.** This item's change moved `envel/cli.py`'s `if result.changed:` from line 165
to line **217**, and three citations still point at 165:

- `tracker/items/WI-0005/artifacts/plan.md:44` — *"saves only when the result reports that it
  changed something [src: envel/cli.py:165]"*
- `tracker/items/WI-0005/artifacts/plan.md:210` — the `## Decisions and ADRs` row for
  *"A refusal writes nothing, because `Ok.changed` gates the save"*
- `docs/architecture/adr/ADR-0011-a-correction-edits-the-entry-in-place.md:101` — `## Decision` 5,
  *"`envel/cli.py` writes nothing, which is how `nothing is changed` is delivered rather than
  promised [src: envel/cli.py:165]"*

All three were **correct when written**: `git show main:envel/cli.py` line 165 is `if
result.changed:`. On the branch head, line 165 is `elif arguments.command == "spend":`. The
citation still resolves — the line exists — so nothing mechanical notices, and the *claim* each
one supports is still true: the save is gated on `result.changed` at `envel/cli.py:217`, which
this execution verified by measuring the store file after every refusal in this report.

It is recorded here rather than acted on, for three reasons. It is not a criterion failure, so it
is not a send-back under this skill's own test — no acceptance criterion of `WI-0005` says
anything about a line number. It is not a defect in behaviour delivered by another item, so it is
not a bug. And this skill writes no document, ever, so the edit is not mine to make
[src: toolkit: verify/contract.md exit criteria "A document it found wrong is a question or a send-back - an execution that may repair what it judges has made the judgement circular"]. The structural point underneath it is worth more than the three
citations: `ADR-0011` was **written by this item's own `plan`** and is therefore in no
invalidation set — the set lists documents the change could make false, and a document the plan
writes from the design it is about is not on it. That is the hole the drift fell through, and it
will recur on any item whose plan cites a line its own implementation then moves.

One thing was looked at closely and deliberately **not** filed: `envel entries --month 2026-01`
lists a spend whose date was corrected to a month before its envelope existed, while
`envel summary 2026-01` for the same store prints `no envelopes existed in 2026-01`. That is not
this item's, and it is not new. It is reachable on `main` without any correction at all — verified
by building a store in a worktree at `main` and running `envel spend groceries 5.00 --on
2026-01-05`, which produces exactly the same pair of outputs. It is the intersection of
[src: WI-0003 AC7 "The summary shows a row for every envelope that existed by the end of the month"]
with `WI-0006`'s listing, and neither criterion is false: the summary shows every envelope that
existed, and the listing covers the month. No criterion of any item says a summary must cover a
month in which the envelope did not exist, so filing a bug here would be legislating rather than
reporting.

## Not verified, and why

- **`envel fix " 4 "` — a reference with surrounding whitespace — succeeds**, because `int()`
  strips it. No criterion speaks to it either way; AC1 promises a refusal for a reference that
  *matches no entry*, and this one matches. Recorded as an observation, not checked as a
  criterion.
- **The three combinations the item deliberately leaves unconstrained** were run, but have no
  criterion to be verified against, so they carry no verdict: a correction to the value the entry
  already has (succeeds and prints), `--envelope` naming the envelope the entry is already in
  (succeeds and prints the single-envelope line), and `--on` setting a date before the envelope
  existed (succeeds). `refine` recorded all three in the item's R10 table and `implement` declares
  them; this execution confirms all three behave as declared and none of them writes anything
  surprising.
- **AC19's six uncovered combinations have no standing executable case.** Verified here by hand
  and waived by name above, with the structural reason. A reader who wants a regression guard for
  them wants six more CLI cases, which is a test-coverage decision rather than a defect.
- **AC8's month-crossing case cannot be observed against a store built only by the delivered
  commands**, because `envel new` stamps `created` with today. The store's envelope timestamps
  were edited by hand for that case. This is the observation AC8 names, made against a store whose
  *setup* was seeded rather than typed — the correction itself, and both summaries, are the
  tool's.
- **Nothing about durability beyond a process boundary.** AC14 asks for separate invocations with
  the process exiting between them, and that is what was run. Nothing here tests a power failure
  mid-write; `ADR-0002`'s atomic-replace claim is outside this item's criteria and was not
  re-verified.
