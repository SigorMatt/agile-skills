# Verification report — WI-0003

Verified-commit: f6b37ed89b5a6274f41213b19a959ddc6f98e88a

## Verdict

**Pass.** All twelve acceptance criteria were checked by running commands against the branch head
and reading the actual output; all twelve pass. The three properties `ADR-0004` promises were
checked beyond the criteria's own examples: over seven hand-built records and over **400
randomly generated ones**, every settlement zeroed every position, stayed within the `n - 1`
bound, named nobody at zero, and reproduced itself exactly.

Thirteen mutations of my own choosing were run against the suite. Ten were caught, **three
survived**: one is behaviour-preserving, and **two are real gaps in the tests** — the ordering
contract of `net_positions` is unasserted, and AC10's record has only one expense, so a rewrite
that merely reorders would pass it. Neither is a criterion failure and neither is a send-back, but
both are findings and both are recorded below rather than rounded off.

The criteria were read and every check derived from them before `impl-report.md` was opened.

## Criteria

Commands were run from the project root against a fresh `EXPENSES_FILE`. `|` marks a line break.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `who-owes-whom` with no people and no record file | exit `0`, stdout `Everybody is settled up.`, stderr empty | the file does not exist at this point |
| AC2 | **pass** | four people added, then `who-owes-whom` | exit `0`, same line, stderr empty | |
| AC3 | **pass** | the two balancing expenses from the criterion, then `who-owes-whom` | exit `0`, same line | positions are all zero, checked directly: `{Alice: 0, Bob: 0, …}` |
| AC4 | **pass** | `add-expense 30 --paid-by Alice --shared-by Alice,Bob,Carol`, then `who-owes-whom` | `Bob pays Alice 10.00` then `Carol pays Alice 10.00`, exit `0` | the tie is genuinely decided by name — see the two probes below |
| AC5 | **pass** | `add-expense 10 --paid-by Alice --shared-by Alice,Bob,Carol`, then `who-owes-whom` | `Bob pays Alice 3.33` then `Carol pays Alice 3.33`, exit `0` | positions read directly: `Alice 666, Bob -333, Carol -333`; the two transfers come to 666 exactly |
| AC6 | **pass** | the two expenses from the criterion, then `who-owes-whom` | exactly `Carol pays Alice 15.00`, exit `0` | Carol and Alice share no expense |
| AC7 | **pass** | seven hand-built records **and** 400 random ones; each transfer applied to the net positions | every position `0` afterwards, in every case | the seven include one debtor with two creditors, two debtors with two creditors, a five-person three-expense record and a payer who shares nothing |
| AC8 | **pass** | the same 407 records | transfers ≤ `nonzero - 1` in every case; e.g. five people with non-zero positions → four transfers | |
| AC9 | **pass** | `who-owes-whom` three times, three separate processes, output compared | identical all three times | the randomised check also re-ran `settle` on each of its 400 records and got the same list |
| AC10 | **pass, with a caveat** | `md5sum` of the record before and after `who-owes-whom` | unchanged (`a23c62fe…`) | the caveat is Finding 2: the assertion is weaker than it looks |
| AC11 | **pass** | `who-owes-whom extra` | exit `1`, stderr `who-owes-whom takes no arguments.`, stdout empty, no traceback | |
| AC12 | **pass** | AC6's record; Bob's position read directly as `0` | `Bob` appears nowhere in the output | also checked automatically on all 407 records: no zero-position person is ever named |

### The tie-break, probed three ways

The order in AC4 is the only thing distinguishing two otherwise-valid outputs, and it is easy to
produce by accident. Three probes:

| probe | output | what it shows |
|-------|--------|---------------|
| `Carol` added **before** `Bob`, then AC4's expense | `Bob pays Alice 10.00` first | the order is the name's doing, not insertion order — a stable sort with no name comparison would have printed Carol first |
| people added as `CAROL`, `alice`, `bob` | `bob pays alice 10.00` then `CAROL pays alice 10.00` | the key is case-folded, as `ADR-0005` point 3 requires; comparing raw spellings would put `CAROL` first |
| two creditors owed the same — `Zoe` and `Alice`, with `Bob` owing 30 | `Bob pays Alice 15.00` then `Bob pays Zoe 15.00` | the tie-break applies on the **creditor** side too, which no criterion example exercises |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q`, run here at `f6b37ed` → exit `0`, `Ran 96 tests in 1.814s`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses tests` → exit `0`. `ADR-0008`: a syntax check, not a linter |
| `workspace-valid` | **pass** | `validate-workspace` → exit `0`, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the table above; no row cites `impl-report.md`, and the 407-record property check is evidence the criteria's own examples cannot supply |
| `negative-cases-exercised` | **pass** | AC11 triggered; four boundary probes below, including a corrupt record and a hand-edited one whose positions do not sum to zero |
| `tests-would-fail-without-the-change` (advisory) | **pass, with three survivors** | thirteen mutations, ten caught, three analysed below — two of them real gaps |

## Negative and boundary cases exercised

| probe | result |
|-------|--------|
| record file contains `not json` | exit `1`, `<path> is not valid JSON; it has not been changed.`, no traceback — `ADR-0007` point 5 holds for this subcommand too |
| **hand-edited record whose positions do not sum to zero** — one expense of 1.00 with two stated shares of 1.00 each | exit `0`, output `Everybody is settled up.`, while `net_positions` reports `Alice 0, Bob -100`. Bob is a pound down and the tool says everybody is square. See Finding 1 |
| a payer who shares nothing (`9.00 --paid-by Alice --shared-by Bob,Carol`) | `Bob pays Alice 4.50` then `Carol pays Alice 4.50` — correct |
| the smallest divisible expense (`0.03` split three ways) inside the random set | settles exactly, no transfer of `0.00` ever emitted in 400 records |

## Test sensitivity check

Thirteen mutations, chosen to attack different code paths from the implementation report's set —
reversing the emitted order, inverting each tie-break separately, rounding transfers to 10p,
printing raw minor units, forgetting to reduce the creditor, doubling the payer's outlay, and
three aimed at the properties. Each was applied to the real source, run against the whole suite,
and reverted; `git status -- expenses tests` is clean afterwards and the suite is green.

**Ten were caught.** Worth noting: the creditor-side tie-break is caught by exactly **one** test,
`test_one_debtor_owing_two_creditors_splits_the_payment` — the test added after a mutation escaped
during implementation. Without it, both creditor-side mutations would have survived. And rounding
transfers to 10p made the suite **hang**, because the loop can no longer reduce a position below
10p; that is a caught mutation, but it is worth knowing that this loop's failure mode is a hang
rather than a wrong answer.

**Three survived:**

1. **Keeping zero-position people in `settle`'s working set** — behaviour-preserving, as
   `impl-report.md` says. The extremes are unaffected by zeros and the loop's guard fires when
   only zeros remain. Not a gap. (My mutation's label claimed it also dropped the guard; it did
   not — the replacement only removed the filter. Recorded so the label is not read as more than
   it was.)
2. **Sorting `net_positions`' result by amount instead of returning people in the order they were
   added** — survives, because nothing observable depends on that order: `settle` builds a dict
   and selects by explicit keys, and every test converts the result to a dict. But `plan.md`
   § *Assumptions* 1 states the order as a contract, and **no test asserts it**. It matters for
   WI-0004, which extends this same function. A real gap, in the tests rather than in the code.
3. **Rewriting the record during `who-owes-whom`** — I made the handler reverse the `expenses`
   list and save it. `test_the_record_is_not_modified` still passed, because its record holds
   **one** expense, and reversing a one-element list changes nothing. I confirmed the mechanism
   directly: with two expenses, the same mutation does change the file's bytes. So AC10's
   assertion is sound but its fixture is too small to exercise it. Again a gap in the tests, not
   in the code — `_who_owes_whom` genuinely never calls `save`, which I confirmed by reading it.

## Defects found

None against any acceptance criterion. Three findings, none of which routes to a send-back or a
bug — the first is behaviour no criterion covers, and the other two are test-coverage gaps in
behaviour that is correct today:

1. **A hand-edited record whose positions do not sum to zero produces `Everybody is settled up.`**
   The plan predicted "a short, wrong settlement"; the actual behaviour is worse-sounding and
   worth having on the record: with `Alice 0, Bob -100`, the tool prints that everybody is square
   while Bob is a pound out of pocket. `plan.md` § *Risks* records this as deliberately unguarded
   and forbids `implement` from adding a guard on its own initiative, which it correctly did not.
   No criterion covers it and the tool cannot write such a record itself.
2. **`net_positions`' documented ordering is unasserted** (survivor 2 above). WI-0004 extends this
   function; if it reorders while doing so, nothing fails.
3. **AC10's test record has one expense** (survivor 3 above), so it cannot distinguish "does not
   write" from "writes something identical or merely reordered".

## Not verified, and why

- **That `who-owes-whom` performs no write at all**, as opposed to no *observable* write. AC10
  compares bytes, and Finding 3 shows what that misses. What I did instead was read
  `_who_owes_whom` — eleven lines, one `storage.load()`, no `storage.save()` — which is assurance
  by inspection, not by test, and is recorded as such.
- **The `n - 1` bound as a proof.** It was checked on 407 records, not proved. `ADR-0004`'s
  argument — each transfer zeroes at least one person — is sound, and the loop matches it, but
  this verification is empirical.
- **Provable minimality**, which `ADR-0004` explicitly does not promise and which the item places
  out of scope. Nothing here checks that the settlement is the smallest possible, and on the
  "two debtors, two creditors" record it prints three transfers where a human might find two.
  That is expected, not a defect.
- **Concurrency and atomicity**, unchanged from WI-0001 and WI-0002; this subcommand writes
  nothing, so neither applies to it.
- **`lint-clean` covers syntax only** (`ADR-0008`); roughly ninety new lines went through this
  item with review as the only style check.
