# Verification report — WI-0004

Verified-commit: f3be13cb4d0515a9a66587a9017cba120042205c

## Verdict

**Pass.** All fifteen acceptance criteria were checked by running commands against the branch head
and reading the actual output; all fifteen pass.

**The three gaps two earlier reviews handed to this item are genuinely closed.** I checked that
the only way it can be checked — by re-running the three mutations that survived on WI-0002 and
WI-0003 against this branch. All three now fail a test, each the test written for it.

Ten mutations of my own were run beyond those three. Nine were caught; **one survived**, and it is
a real coverage gap: nothing exercises a corrupt `payments` key, so removing the shape check that
`plan.md` step 1 required passes the whole suite. The code is right — I confirmed the behaviour by
probe — but no test would notice it going away. Not a criterion failure and not a send-back;
recorded as a finding.

The criteria were read and every check derived from them before `impl-report.md` was opened.

## Criteria

Commands were run from the project root against a fresh `EXPENSES_FILE`, with `Alice`, `Bob`,
`Carol` and `Sam Okafor` added first. `|` marks a line break.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `add-payment 10 --from Bob --to Alice` | exit `0`, stdout `Recorded 10.00 paid by Bob to Alice.`, stderr empty | |
| AC2 | **pass** | five separate processes: three `add-person`, `add-expense`, `add-payment`, then `payments` and `who-owes-whom` | the later invocations print `1. Bob paid Alice 10.00` and `Carol pays Alice 10.00` | the effect on the settlement survives the process boundary, not just the payment |
| AC3 | **pass** | `payments` after one payment, then after a second | `1. Bob paid Alice 10.00`; then that plus `2. Carol paid Sam Okafor 2.50` | numbering, order, two decimals, past tense, stored spellings |
| AC4 | **pass** | `payments` on a fresh record | exit `0`, `No payments have been recorded yet.`, stderr empty | |
| AC5 | **pass** | the expense, `who-owes-whom`, the payment, `who-owes-whom` | `Bob pays Alice 10.00`+`Carol pays Alice 10.00` before; exactly `Carol pays Alice 10.00` after | the before-and-after is what makes this criterion mean anything |
| AC6 | **pass** | the expense, `add-payment 4 --from Bob --to Alice`, `who-owes-whom` | exactly `Carol pays Alice 10.00` then `Bob pays Alice 6.00` | Carol leads: her debt is now the larger |
| AC7 | **pass** | both payments, `who-owes-whom` | exactly `Everybody is settled up.`, exit `0` | |
| AC8 | **pass** | `add-payment 30 --from Bob --to Alice`, `who-owes-whom` | the payment exits `0`; then exactly `Alice pays Bob 10.00` then `Carol pays Bob 10.00` | overpayment accepted, direction reversed, Alice first on the tie |
| AC9 | **pass** | `--from Dave`; `--to Dave`; `--from "sam okafor"` | `Dave is not in the group.` twice, exit `1`; the third exits `0` and lists `1. Sam Okafor paid Alice 10.00` | after the refusals, `payments` is empty and `people` still lists four |
| AC10 | **pass** | `--from Alice --to Alice`; `--from ALICE --to Alice`; `--from "  alice  " --to Alice` | all three exit `1` with `A payment must be between two different people.` | sameness is the identity key, including whitespace |
| AC11 | **pass** | `ten`, `10.005`, `0`, `-5` | `ten is not an amount.`; `Amounts have at most two decimal places: 10.005.`; `A payment must be for more than zero.` twice | |
| AC12 | **pass** | the criterion's six command lines | `add-payment needs an amount.`; `… needs --from.`; `… needs --to.`; `--from was given more than once.`; `Unknown option: --for.`; `payments takes no arguments.` | |
| AC13 | **pass** | twelve refusals against a record holding an expense and a payment, comparing `payments`, `expenses`, `people`, `who-owes-whom` **and the file's md5** before and after | identical; no refusal exited `0`; no stderr contained a traceback | **and the last clause**: on a record with no file, three refusals left no file behind |
| AC14 | **pass** | `people` and `expenses` after AC5's record | `Alice`,`Bob`,`Carol`,`Sam Okafor`; `1. 30.00 paid by Alice, shared by Alice 10.00, Bob 10.00, Carol 10.00` | unchanged by the payment |
| AC15 | **pass** | one payment, no expenses, `who-owes-whom` | exactly `Alice pays Bob 10.00` | |

The stored record was read directly and matches `ADR-0011` point 1 field by field:
`{"amount": 1000, "from": "Bob", "to": "Alice"}`, amount in minor units, both names as stored.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q`, run here at `f3be13c` → exit `0`, `Ran 115 tests in 1.353s`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit `0` (`ADR-0008`: a syntax check) |
| `workspace-valid` | **pass** | `validate-workspace` → exit `0`, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the table above; no row cites `impl-report.md` |
| `negative-cases-exercised` | **pass** | AC9–AC13 all triggered, twelve refusals in sequence against a populated record and three against an empty one, plus seven boundary probes below |
| `tests-would-fail-without-the-change` (advisory) | **pass, with one survivor** | thirteen mutations — the three inherited ones plus ten of my own; twelve caught, one survivor analysed below |

## Negative and boundary cases exercised

| probe | result |
|-------|--------|
| a WI-0003-era record with **no `payments` key** | `payments` prints the empty message, `who-owes-whom` works, `add-payment` then works and settles — `ADR-0007` point 2 holds for the fourth key too |
| `"payments": "nope"` | exit `1`, `The payments in <path> are not in the expected shape; it has not been changed.` |
| a payment with `"amount": "ten"` | refused the same way, and the file is byte-identical afterwards |
| a payment with a missing `to` field | refused the same way |
| a payment naming somebody not in `people` (hand-edited) | `Alice pays Ghost 1.00`, exit `0` — nothing validates the reference, exactly as for expenses; the tool cannot write such a record |
| unwritable directory, with people already added | exit `1`, `Cannot save to <path>: Permission denied.`, **no traceback** — `ADR-0010` covers `add-payment` for free, because the catch is in `cli.main` |
| twelve refusals in sequence, then the file's md5 | unchanged |

## Test sensitivity check

Thirteen mutations, each applied to the real source, run against the whole suite, reverted;
`git status -- expenses tests` clean afterwards and the suite green.

**The three inherited gaps — the point of this check:**

| mutation | on the item that recorded it | on this branch |
|----------|------------------------------|----------------|
| save the record before validating, so a refusal creates a file | survived on WI-0002 | **caught** — `test_a_refused_payment_leaves_no_record_file_behind` |
| `net_positions` returns people sorted by amount instead of insertion order | survived on WI-0003 | **caught** — `test_everybody_is_returned_in_the_order_they_were_added` |
| `who-owes-whom` reorders and rewrites the record | survived on WI-0003 | **caught** — `test_the_record_is_not_modified`, on the two-expense two-payment fixture |

I also tried a fourth in the same family — `net_positions` dropping people at zero — and it is
caught by four tests, so the contract is asserted in both of its parts.

**Nine of my own ten were caught:** the sign of the recipient's adjustment (2 tests), numbering
payments from 0 (3), comparing raw spellings instead of identity keys in the self-payment check
(2), resolving the payer without `find_person` (3), refusing an overpayment (1), and the four
above.

**One survived: removing the `payments` shape check in `storage.load` entirely.** Nothing in the
suite feeds the tool a corrupt `payments` key, so `plan.md` step 1's requirement — mirroring
`_is_expense` — is unasserted. WI-0002 has `RecordCompatibilityTest` for the equivalent on
expenses; this item has no counterpart. The behaviour itself is correct: I fed it four malformed
records by hand (see the probes above) and each was refused with the right message and left the
file untouched.

## Defects found

None against any acceptance criterion. One finding:

1. **The `payments` shape check is unasserted.** `ADR-0011` point 5 and `plan.md` step 1 both
   require it, the code implements it correctly, and no test would notice it being deleted. It is
   not a criterion failure — no criterion on this item mentions a corrupt record — and not a bug
   against another item, since this is behaviour WI-0004 itself introduced. It is the same species
   as the two gaps this item was created to close, which is worth saying plainly: the pattern that
   produced them is still producing them, and it is *a plan step with no criterion behind it*.

## Not verified, and why

- **Duplicate payments.** Recording the same payment twice is indistinguishable from two real
  payments and the tool believes it. `ADR-0011` § *Consequences*, `plan.md` § *Risks* and
  `impl-report.md` all say so. No criterion covers it and nothing checks it.
- **A hand-edited payment naming somebody outside the group** produces a transfer with that name
  in it. Probed above; the same behaviour as for expenses (WI-0003 recorded it), and no criterion
  covers it.
- **Atomicity of the write** — unchanged since WI-0001: argued from `os.replace`, not
  demonstrated. The consequence that matters, that an unreadable record is never overwritten, was
  demonstrated again here on four malformed files.
- **Concurrent writers** — excluded by `docs/product/vision.md` (v3).
- **`lint-clean` covers syntax only** (`ADR-0008`); around 120 new lines went through this item
  with review as the only style check.
- **`group.__all__`** now lists eleven names and nothing imports `*` anywhere in the project, so
  the list is documentation rather than machinery. `impl-report.md` declares having corrected it;
  I confirmed it matches the module's public functions, but nothing exercises it.
