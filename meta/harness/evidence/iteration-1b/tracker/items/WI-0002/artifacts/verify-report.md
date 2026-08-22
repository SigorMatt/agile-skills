# Verification report — WI-0002

Verified-commit: 10a6bc3948881181afc41c5d2b2c2b924f30ec86

## Verdict

**Pass.** All fourteen acceptance criteria were checked by running commands against the branch head
and reading the actual output; all fourteen pass. Coverage was measured with fifteen mutations of
my own choosing, one per criterion, chosen deliberately to attack different code paths from the
seventeen the implementation report describes. Thirteen were caught; **two survived**, and both are
behaviour-preserving with respect to every observable any criterion pins — the analysis is below,
because "all mutations caught" would have been the easier and less true thing to write.

No criterion failed, so nothing is sent back. Three findings are recorded, none of them a defect
against a criterion; the sharpest is a grammatical wart in a message no criterion pins.

The criteria were read and every check derived from them before `impl-report.md` was opened.

## Criteria

Every command was run from the project root against a fresh `EXPENSES_FILE` in a temporary
directory, with `Alice`, `Bob`, `Carol` and `Sam Okafor` added first, as the criteria specify.
Output is quoted as captured; `|` marks a line break.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `add-expense 30 --paid-by Alice --shared-by Alice,Bob,Carol` | exit `0`, stdout `Recorded 30.00 paid by Alice, shared by 3 people.`, stderr empty | matched byte for byte with `cat -A` |
| AC2 | **pass** | `add-expense 30 …`, then `add-expense 12 …`, then `expenses` — three separate processes | the third prints `1. 30.00 paid by Alice, …` and `2. 12.00 paid by Bob, shared by Bob 12.00`, exit `0` | three real invocations, not three calls into one process |
| AC3 | **pass** | `expenses` after AC1 | exit `0`, stdout exactly `1. 30.00 paid by Alice, shared by Alice 10.00, Bob 10.00, Carol 10.00` | numbering, order, two decimals and stored spellings all as pinned; `--paid-by "sam okafor"` lists as `Sam Okafor` |
| AC4 | **pass** | `expenses` on a fresh record | exit `0`, stdout `No expenses have been recorded yet.`, stderr empty | the record file does not exist at that point, so "missing file" is covered too |
| AC5 | **pass** | `add-expense 12 --paid-by Alice --shared-by Bob`, then `expenses` | `1. 12.00 paid by Alice, shared by Bob 12.00` | one sharer takes the whole total, and the payer is not a sharer |
| AC6 | **pass** | `add-expense 30 --paid-by Alice --shared-by Alice,Bob=6,Carol`; and `add-expense 10 … --shared-by Alice=10,Bob` | `1. 30.00 paid by Alice, shared by Alice 12.00, Bob 6.00, Carol 12.00`; `1. 10.00 paid by Alice, shared by Alice 10.00, Bob 0.00` | both examples verbatim, including the `0.00` share |
| AC7 | **pass** | the criterion's three command lines | `Alice 3.34, Bob 3.33, Carol 3.33`; `paid by Sam Okafor, shared by Alice 3.34, …`; `paid by Bob, shared by Alice 4.50, Bob 4.51, Carol 1.00` | the third is the one that matters — the payer is named second and still takes the odd penny, and only the unstated sharers divide the remainder |
| AC8 | **pass** | `--paid-by Dave …`; `--shared-by Alice,Dave`; `--paid-by "sam okafor" …` | `Dave is not in the group.` twice, exit `1`; the third exits `0` and lists `paid by Sam Okafor` | after the refusals, `expenses` prints the empty-list message and `people` still lists four names — no person and no expense created |
| AC9 | **pass** | the criterion's five command lines, plus `-5` | `twelve is not an amount.`; `Amounts have at most two decimal places: 12.505.`; `An expense must be for more than zero.` (for both `0` and `-5`); `A stated share cannot be negative: Alice=-5.`; `Amounts have at most two decimal places: 1.005.` | each exit `1`, stdout empty |
| AC10 | **pass** | `--shared-by Alice=6,Bob=7`; `Alice=2,Bob=3`; `Alice=4,Bob=6` | `The stated shares come to 13.00, which is more than the total of 10.00.`; `… come to 5.00, which is less than the total of 10.00, and every sharer has a stated share.`; the third exits `0` and lists `Alice 4.00, Bob 6.00` | the accepted case is the one an over-eager check would break |
| AC11 | **pass** | the criterion's five forms, and `Alice,ALICE` | `--shared-by needs at least one name.`; `A name cannot be empty.`; `Bob= has no amount after the equals sign.`; `Alice=1=2 has more than one equals sign.`; `Alice is named twice in --shared-by.` for both spellings | each exit `1` |
| AC12 | **pass** | the criterion's six command lines | `add-expense needs a total.`; `add-expense needs --paid-by.`; `add-expense needs --shared-by.`; `--paid-by was given more than once.`; `Unknown option: --split-by.`; `expenses takes no arguments.` | each exit `1`, stdout empty |
| AC13 | **pass** | all twenty refusals above, then `expenses` and `people`; and separately, five refusals against a record already holding two expenses | the listing is byte-identical before and after (`[ "$before" = "$after" ]` → true); `people` unchanged; no stderr contains `Traceback (most recent call last)` | also checked that a refusal on a record with no file yet does **not** create the file |
| AC14 | **pass** | `people` after AC1 | exit `0`, stdout `Alice`, `Bob`, `Carol`, `Sam Okafor` on four lines | the order they were added, undisturbed |

The stored record was also read directly after AC2 and matches `ADR-0009` exactly: `total` in minor
units (`3000`), `paid_by` as the stored spelling, and `shares` an ordered list of `{"person": …}`
objects with `amount` present only where one was stated. No derived share is stored, which is
`ADR-0003` point 6 confirmed against the file rather than against a document.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q`, run here at `10a6bc3` → exit `0`, `Ran 79 tests in 0.768s`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit `0`. Per `ADR-0008` this is a syntax check, not a linter |
| `workspace-valid` | **pass** | `validate-workspace` → exit `0`, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the table above — every row is a command run during this verification with its captured output; no row cites `impl-report.md`, and the criteria were read first |
| `negative-cases-exercised` | **pass** | all six refusal criteria triggered rather than read about — AC8 (three cases), AC9 (six), AC10 (two refusals plus the acceptance), AC11 (six), AC12 (six), AC13 (twenty in sequence) — plus nine boundary probes below |
| `tests-would-fail-without-the-change` (advisory) | **pass, with two documented survivors** | fifteen mutations, one per criterion, all reverted; thirteen caught, two behaviour-preserving — see below |

## Negative and boundary cases exercised

Beyond the criteria:

| probe | result |
|-------|--------|
| a record written before expenses existed (no `expenses` key) | `expenses` prints the empty-list message, exit `0`; `add-expense` then works — `ADR-0007` point 2 confirmed in the direction that matters |
| `"expenses": "nope"` | exit `1`, `The expenses in <path> are not in the expected shape; it has not been changed.`, and the file is byte-identical afterwards |
| `"total": true` (a bool where an int belongs) | refused the same way — Python's `bool` is an `int`, so a naive check would have let it through and recorded a total of one penny |
| `"shares": []` | refused — `ADR-0002` requires at least one sharer |
| an expense naming a person no longer in `people` (hand-edited) | prints `1. 1.00 paid by Ghost, shared by Ghost 1.00`, exit `0`. Nothing validates the reference; `plan.md` § *Risks* says so and nothing removes a person, so it cannot arise from the tool |
| `999999999.99` split two ways | `Alice 500000000.00, Bob 499999999.99` — sums exactly; integer arithmetic, no float drift |
| `0.01` split three ways | `Alice 0.01, Bob 0.00, Carol 0.00` — the payer takes the only penny and the shares sum to the total |
| `--paid-by` with no value, and `--paid-by --shared-by Alice` | `--paid-by needs a value.`, exit `1` — behaviour no criterion covers; see *Not verified* |
| `add-expense 30 40 …` | `add-expense takes a single total.`, exit `1` — likewise |
| unwritable directory (`ADR-0010`) | `Cannot save to <path>: Permission denied.`, exit `1`, **no traceback** — the WI-0001 gap is closed, though no criterion here asserts it |

No probe produced a traceback, and no probe overwrote a record it could not read.

## Test sensitivity check

Fifteen mutations, one per criterion, chosen to attack different code paths from the ones the
implementation report used — reversing the listing, changing the sharer separator, halving a
stated share, giving the odd penny to the last sharer instead of the first, sorting `people` on
save, and so on. Each was applied to the real source, run against the whole suite, and reverted.
`git status` afterwards shows no modified source file and the suite is green again.

**Thirteen were caught.** The narrowest margins are worth naming: reversing the expense order is
caught by **one** test (`test_expenses_are_numbered_from_one_in_the_order_recorded`), and allowing
an empty element in the sharer list by **one** (`test_an_empty_element`). Everything about the
remainder rule is caught by three or more.

**Two survived, and both are behaviour-preserving:**

1. *Saving the loaded record before validating anything.* Inserting `storage.save(record)` between
   `storage.load()` and `group.add_expense(...)` failed no test. It writes back exactly what was
   read, so no observable any criterion pins changes.
2. *Saving even when `add_expense` raises* (wrapping the call in `try/finally`). Also failed no
   test, for the same reason: `group.add_expense` appends to the record only after every rule has
   passed, so when it raises, the record it would save is the one it loaded.

Both survive because of a design property rather than a gap in the assertions — the append is the
last thing `add_expense` does. I checked that directly with a sharper mutation: **appending the
expense before the two sum checks** — which really does record an invalid expense — was caught by
13 tests. So AC13's "nothing is recorded" is genuinely covered.

The one observable difference either survivor would produce is that a refusal would *create* the
record file where none existed. WI-0001 pins that for `add-person`
(`test_a_refusal_does_not_create_the_record_file`); no criterion pins it for `add-expense`, which
is why the mutation slips through. It is a gap in the criteria, not in the tests, and it is
recorded below rather than silently absorbed.

## Defects found

None against any acceptance criterion. Three findings, none of which is a criterion failure and
none of which I could route to another item as a bug — all three are behaviour this item delivered
that no criterion covers:

1. **`shared by 1 people.`** — the AC5 case prints
   `Recorded 12.00 paid by Alice, shared by 1 people.` AC1 pins that sentence only for its own
   three-sharer case, so nothing is violated; but it is the one piece of output in this item a
   user would call wrong. Not sent back: no criterion of this item says otherwise, and inventing
   one now would be verification writing its own target.
2. **A refusal by `add-expense` is not pinned to leave the record file uncreated**, where the
   equivalent is pinned for `add-person`. Today the behaviour is right — I checked, and no file
   appears — but nothing would catch it changing.
3. **Two command-line behaviours have no criterion**: `--paid-by` with no value and
   `add-expense` with two positionals. Both were declared in advance by `impl-report.md`
   § *Deviations*, both behave sensibly, and both are unverifiable against this item's contract.

## Not verified, and why

- **`ADR-0010`'s write-failure message satisfies no criterion of this item.** `plan.md` declared
  this in advance and `impl-report.md` repeats it. I exercised it anyway — an unwritable directory
  gives `Cannot save to <path>: Permission denied.`, exit `1`, no traceback — but that is a probe,
  not a verdict, and it is recorded here rather than as a passing criterion.
- **The three findings above** are unverified in the same sense: the behaviour exists, I ran it,
  and no criterion makes any of it required.
- **Atomicity of the write** (`ADR-0007` point 4) is still argued from construction rather than
  demonstrated, as in WI-0001. The consequence that matters — a record that cannot be read is
  never overwritten — was demonstrated again here with four hand-written corrupt records.
- **Concurrent writers** remain out of scope (`docs/product/vision.md` v3).
- **`lint-clean` covers syntax only** (`ADR-0008`). Nothing in this project checks style, dead code
  or types; two new modules and roughly 250 new lines went through this item with review as their
  only such check.
