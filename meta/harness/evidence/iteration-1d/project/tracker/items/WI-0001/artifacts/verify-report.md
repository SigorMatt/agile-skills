# Verification report — WI-0001

Verified-commit: 49dd2a0cffdabf33fd4976f9d93bfc62edbc591f

Branch `wi/WI-0001`, working tree clean at the time of verification. Every command below was run
by this skill against that commit; nothing in this report is taken from `impl-report.md`. The
criteria were read and the checks derived from them before the implementation report was opened.

## Verdict

**Pass.** All twelve acceptance criteria are met and are ticked in `item.md`. All twelve
mutation checks confirm the tests are sensitive.

One defect was found that no criterion of this item covers, and it is filed as **BUG-0001**
rather than as a send-back: all three recording commands print their success line on stdout
before the save is attempted, so a failed write reports success and failure in the same run. The
data is genuinely unchanged and the exit code and stderr are correct, which is exactly why
WI-0001's own criteria do not catch it.

## Criteria

Amounts are shown as the tool printed them. `$L` is a scratch ledger under `mktemp -d`; no run
touched a real one.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `add-person Ana`; then `add-person` with each of `ana`, ` Ana `, `ANA`, `Ana`; then with `""`, `"   "`, a tab | `Added Ana.` exit 0. Each duplicate: `error: 'ana' is already recorded as 'Ana'; names match ignoring surrounding whitespace and case`, exit 2. Each blank: `error: a person's name cannot be empty or only whitespace`, exit 2. `people` afterwards prints exactly `Ana` | Ana appears in AC2's listing. All four spellings the criterion names are refused, and the ledger is unchanged after each |
| AC2 | **pass** | `people` on an empty ledger; then after `add-person` of `Ana`, `ben`, `CARA`, `  Dee  ` | Empty: `No people recorded.` exit 0. Then `Ana` / `ben` / `CARA` / `Dee`, one per line, exit 0 | Insertion order, and each in the form first typed. `  Dee  ` lists as `Dee`: surrounding whitespace is trimmed on entry, which is what AC1's matching rule requires the stored form to be |
| AC3 | **pass** | `add-expense --payer Ana --amount 60 --description dinner --shared-by Ana --shared-by Ben`; then `--payer Dan`; `--shared-by Dan`; `--shared-by Ana --shared-by " ana "`; `--description "   "`; `--payer Ana --shared-by Ben --shared-by Cara` | Happy path `Recorded 60.00 paid by Ana for dinner.` exit 0. `error: payer 'Dan' is not a recorded person; add them first` exit 2. `error: sharer 'Dan' is not a recorded person; add them first` exit 2. `error: 'Ana' is named twice among the sharers` exit 2. `error: a description cannot be empty or only whitespace` exit 2. Payer-not-a-sharer: exit 0, stored `sharers: ['Ben', 'Cara']` | The repeated sharer was given as two spellings that match under AC1, and was refused. The payer is not required to share |
| AC4 | **pass** | with Ana and Ben recorded: `add-expense --payer Ana --amount 30 --description taxi` (no `--shared-by`); then `add-person Cara`; then read the file and run `expenses` | Stored `sharers: ['Ana', 'Ben']`. Listing: `2026-08-22  Ana paid 30.00 for taxi — shared by Ana, Ben` | Cara, added afterwards, is not retrospectively a sharer. Sharers are stored by name, not by reference |
| AC5 | **pass** | with Ana, Ben and Cara recorded: `add-expense --payer Ana --amount 60 --description dinner`; then read the ledger; then `add-expense --help` | Record keys are exactly `['amount_minor', 'date', 'description', 'payer', 'sharers']`; `amount_minor: 6000`; `sharers: ['Ana', 'Ben', 'Cara']`. The usage output lists `--payer`, `--amount`, `--description`, `--shared-by`, `--date` and nothing else | One amount, three sharers, no per-person amount anywhere in the record and no option to state one. The criterion says "the single amount 60"; the file holds `6000` minor units, which is that amount in the representation `ADR-0004` fixes. The decidable content — one amount, no per-sharer amount — holds exactly |
| AC6 | **pass** | `add-expense --amount` with `12`, `12.5`, `12.50`; then with each of `0`, `0.00`, `-5`, `+5`, `12.`, `.5`, `12.505`, `1,234.56`, `€12.50`, `abc`, `""`, checking the file's md5 before and after each | Accepted three store `[1200, 1250, 1250]`. All eleven refused: exit 2 each, a stderr line each, and `unchanged=yes` on the md5 each time | `12.5` and `12.50` both store 1250, so they mean the same amount. Every one of the eleven strings the criterion names was run, not reasoned about |
| AC7 | **pass** | `--date 2026-01-05`; then no `--date` (machine local date was `2026-08-22`); then `--date` with each of `22/08/2026`, `2026-8-1`, `2026-13-01`, `2026-02-30`, `today`, and additionally `20260822` | Stored dates `['2026-01-05', '2026-08-22']`. All six refused forms: exit 2, a stderr line, md5 unchanged | The omitted date recorded the machine's current local date. `20260822` is not named by the criterion but is accepted by `date.fromisoformat`; it is refused, so the criterion's "written `YYYY-MM-DD`" is enforced rather than approximated |
| AC8 | **pass** | `expenses` on an empty ledger; then three expenses recorded in an order that is *not* their date order (2026-01-05, 2026-01-06, 2026-01-04) and `expenses` again | Empty: `No expenses recorded.` exit 0. Then three lines in recording order, the 2026-01-04 one last: `2026-01-05  Ana paid 60.00 for dinner — shared by Ana, Ben` / `2026-01-06  Ben paid 7.50 for coffee — shared by Ana` / `2026-01-04  Ana paid 3.00 for snack — shared by Ana, Ben` | Deliberately recorded out of date order to show the listing is in recording order and not silently sorted. All five fields present on each line |
| AC9 | **pass** | `XDG_DATA_HOME=$V/xdg python3 -m expenses add-person Ana` then `people` with the same environment, and again from a different working directory; `HOME=$V/home` with `XDG_DATA_HOME` unset; `--file $V/trip.json` then the default listing; `--file` at two paths; `--file $V/deep/nested/l.json`; `--file $V/never.json people`; a directory at mode 500; a file at mode 000; a file containing `{not json` | Default: `Added Ana.` / `Ana`, file created at `$V/xdg/expenses/ledger.json`, same answer from `/tmp`. With `HOME` redirected the path used was `…/home/.local/share/expenses/ledger.json`. `--file $V/trip.json add-person Trippy` then the default listing prints `Ana` only. `trip.json` → `Trippy`; `flat.json` → `No people recorded.`. Nested path created, exit 0. Never-written path: `No people recorded.` exit 0, **no file created**. Mode 500 dir: `error: cannot write the ledger at …: [Errno 13] Permission denied`, exit 1. Mode 000 file: `error: cannot read the ledger at …`, exit 1, md5 unchanged. Corrupt file: `error: the ledger at … is not valid JSON`, exit 1, md5 unchanged | Every clause of the criterion exercised. Run as uid 1000, so the permission cases are real. A corrupt ledger is refused rather than silently overwritten with an empty one — not required by any criterion, but the opposite would destroy data |
| AC10 | **pass** | three `add-person`, two `add-expense`, one `repay`, each its own `python3 -m expenses` process; then each of `people`, `expenses`, `repayments` run twice more, each in a fresh process, output captured to files and compared with `cmp` | All three pairs `identical: yes`. `people` → `Ana` / `ben` / `Cara`; `expenses` → two lines with the same dates, payers, amounts, descriptions and sharers; `repayments` → `2026-01-07  Cara repaid 20.00 to Ana` | Every listing came from a process that never saw the recording process. Same fields, same order |
| AC11 | **pass** | `repay --from Ana --to Ben --amount 20` with no expenses recorded; `--to` as each of `Ana`, `ana`, ` ANA ` against `--from Ana`; `--from Dan`; `--to Dan`; `--amount 12.505`; `--amount 0`; `--date 22/08/2026`; `repay --from " ben " --to ANA --amount 12.5 --date 2026-01-05` | `Recorded Ana repaying 20.00 to Ben.` exit 0 with no expense behind it. All three self-repayment spellings: `error: 'Ana' cannot repay themselves` exit 2, md5 unchanged. `error: payer 'Dan' is not a recorded person` / `error: payee 'Dan' is not a recorded person`, exit 2. Amount and date refusals identical in wording to AC6's and AC7's. The last stored as `{'date': '2026-01-05', 'from': 'Ben', 'to': 'Ana', 'amount_minor': 1250}` | The amount goes through the same validator as AC6 and the date the same as AC7, checked by running AC6 and AC7 refusals through `repay` rather than by reading the code. Names are stored in the recorded display form |
| AC12 | **pass** | `repayments` on an empty ledger; then one expense described `unmistakable-dinner` and three repayments dated 01-06, 01-07, 01-08; then `repayments`, `expenses`, and `grep` across both | Empty: `No repayments recorded.` exit 0. Then `2026-01-06  Ben repaid 17.13 to Ana` / `2026-01-07  Ana repaid 1.00 to Ben` / `2026-01-08  Ben repaid 2.00 to Ana`. The expense listing contains `17.13` zero times; the repayment listing contains `unmistakable-dinner` zero times | Date, who paid whom, and how much on each line, in recording order. Neither listing shows the other kind, per `ADR-0001`. The amounts and description were chosen to be unmistakable so the greps could not pass by coincidence |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` on the branch head → exit 0, `Ran 83 tests in 2.333s`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit 0. `ADR-0005` records that this is a syntax check standing in for a linter, so green means every file parses and nothing more — see `## Not verified, and why` |
| `workspace-valid` | **pass** | `.claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the table above gives, for each of AC1–AC12, the command this skill ran and the output it produced. No row cites `impl-report.md` |
| `negative-cases-exercised` | **pass** | see the section below — 41 distinct refusals triggered, each with its exit code and, where the criterion requires it, an md5 comparison of the ledger before and after |
| `tests-would-fail-without-the-change` (advisory) | **pass** | twelve mutations, one per criterion; every one turned the suite red — see the section below |

## Negative and boundary cases exercised

Each of these was triggered, not read about.

- **AC1** — four duplicate spellings (`ana`, ` Ana `, `ANA`, `Ana`) and three blank names (empty,
  spaces, a tab). Seven refusals.
- **AC2, AC8, AC12** — the empty listing for all three commands: a line saying so, exit 0, and no
  file created where none existed.
- **AC3** — unrecorded payer, unrecorded sharer, the same person as two matching spellings among
  the sharers, and a whitespace-only description. Four refusals.
- **AC4** — the boundary the criterion is about: a person added *after* the expense was recorded,
  confirmed absent from the stored sharers and from the listing.
- **AC6** — all eleven refused amount forms the criterion names, each through the CLI, each with
  the ledger's md5 compared before and after; plus the same through `repay`.
- **AC7** — all five refused date forms the criterion names, plus `20260822`, which the criterion
  does not name but which `date.fromisoformat` would accept.
- **AC8** — three expenses recorded deliberately out of date order, to catch a hidden sort.
- **AC9** — a directory at mode 500 (write refused), a file at mode 000 (read refused), a file
  containing `{not json` (parse refused), a path whose parents do not exist (created), and a path
  never written (listed as empty, and **not** created). Run as uid 1000, so the permission bits
  are enforced.
- **AC11** — three self-repayment spellings, an unrecorded person on each side, a bad amount and a
  bad date.

Every refusal was checked against all three parts of this item's definition of the word: a stderr
message naming what was wrong, a non-zero exit code, and — wherever a ledger already existed — an
unchanged file, compared by md5.

## Test sensitivity check

Twelve mutations, one per criterion, each applied to the source, the full suite run, and the
source restored. Every mutation was caught; the suite was green again afterwards.

| AC | what was broken | result |
|----|-----------------|--------|
| AC1 | `find_person` compares raw names instead of normalised ones | FAILED (23 failures, 7 errors) |
| AC2 | `people` prints in reverse order | FAILED (3 failures) |
| AC3 | the repeated-sharer check is bypassed | FAILED (1 failure) |
| AC4 | an expense with no `--shared-by` gets one sharer instead of everyone | FAILED (3 failures) |
| AC5 | a `share_each_minor` key is added to the stored expense | FAILED (1 failure) |
| AC6 | the amount grammar is relaxed to three decimal places | FAILED (4 failures) |
| AC7 | the `YYYY-MM-DD` shape check is bypassed | FAILED (1 failure) |
| AC8 | the expense listing drops the description | FAILED (4 failures) |
| AC9 | `resolve_path` ignores `--file` | FAILED (41 failures, 1 error) |
| AC10 | repayments are dropped when the ledger is serialised | FAILED (6 failures, 4 errors) |
| AC11 | the self-repayment check is bypassed | FAILED (3 failures) |
| AC12 | the repayment listing also prints expenses | FAILED (2 failures) |

`git status --short` was empty afterwards and the restored suite exits 0, so nothing from this
check remains in the tree.

## Defects found

- **BUG-0001 — a failed ledger write still prints the success line on stdout.** Filed at `ready`
  under `EP-001` with `found-in: WI-0001`, priority medium. `add-person`, `add-expense` and
  `repay` all print their success line before `main` attempts the save, so a write failure emits
  both a success line on stdout and an error on stderr, and exits 1. `expenses/cli.py`'s own
  module docstring states the intended order as "…save atomically, print, return 0", so this is a
  slip against the stated design. Filed as a bug rather than a send-back because no acceptance
  criterion of WI-0001 constrains stdout on a failed write: the criteria's definition of "refused"
  is a stderr message, a non-zero exit, and unchanged data, and all three hold.

Nothing else was found. The diff was read against `plan.md` and every file traces to a plan step:
five modules under `expenses/`, six test files, and `docs/architecture/overview.md`. The five
deviations `impl-report.md` declares were each checked against the plan and are accurate; none
changes what is delivered.

## Not verified, and why

- **The real default ledger location was never written to.** AC9's default-location clauses were
  verified with `XDG_DATA_HOME` and then `HOME` pointed at scratch directories, which is what the
  tool sees as "no location given". The path an unmodified environment would use —
  `~/.local/share/expenses/ledger.json` — was confirmed by redirecting `HOME` and observing the
  path, not by writing to the operator's own home. A reader who wants the literal default written
  can run one `add-person` with no `--file` and no environment override.
- **`lint-clean` proves only that every file parses.** No style or type checker is installed
  (`ADR-0005`), so unused imports, shadowed names and type errors are outside every gate this
  pipeline runs. Read the green result as "it compiles".
- **Concurrency was not exercised.** `impl-report.md` declares that two simultaneous writers can
  lose an update; no criterion covers it and no test drives it, so this report neither confirms
  nor refutes it. It remains a declared, unverified property.
- **The on-disk `version` field is written and never read.** Confirmed by reading `store.load`,
  not by a behavioural test — there is no second version to write, so there is nothing to
  observe. A ledger written by a future incompatible version would be read as if it were version 1
  rather than refused.
- **Very large ledgers were not tested.** Every check here used a handful of records. The
  whole-file-rewrite cost `ADR-0003` records as a risk is untested at any scale.
- **AC5's phrase "the single amount 60"** was judged satisfied by `amount_minor: 6000`, on
  `ADR-0004`, which fixes minor units as the representation. This is recorded rather than treated
  as ambiguous because the criterion's decidable content — one amount, no per-sharer amount — is
  unaffected by the representation, and both readings agree on it.
